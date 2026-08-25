#!/usr/bin/env bash
# Quenched campaign on SDumont2.  One script drives both stages; the stage is
# chosen with CAMPAIGN_KIND=generate|fracture.
#
#     source Code/cluster/sdumont2nd/env.sh
#     Code/Fracture_fibril/slurm/make_manifest.sh generate
#     CAMPAIGN_KIND=generate Code/Fracture_fibril/slurm/submit_campaign.sh
#
# Shape: several medium tasks that BACKFILL.  The QOS caps the account at 1920
# CPUs and at 100 running jobs, but the binding constraint in practice is the
# partition: cpu_amd is routinely at zero idle nodes with a long queue from
# other users.  Asking for whole nodes (--exclusive) means waiting behind every
# job already queued, so tasks request a fraction of a node instead and start on
# the free cores of a partially used one.  Each task takes a contiguous slice of
# the manifest and runs it with xargs -P (GNU parallel is not assumed).

#SBATCH --job-name=dla-campaign
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=24:00:00
# No --output/--error here on purpose: submit_campaign.sh passes ABSOLUTE paths.
# Slurm opens these files at launch time, and a relative path resolves against
# the submit directory as seen from the compute node.  On Lustre that directory
# may not be visible yet when the task starts, and the launch then fails with
# "launch failed requeued held" -- producing no log at all, which is exactly
# what makes the failure so hard to read.

set -euo pipefail

repo="${DLA_REPO:-$HOME/gitrepos/dla-collagen}"
# On the cluster this configures the module, the venv and the paths.  If the
# environment is already configured (DLA_PROJECT set), it is left alone, which
# is what lets these scripts be exercised off-cluster before submission.
if [[ -z "${DLA_PROJECT:-}" ]]; then
    # shellcheck source=../../cluster/sdumont2nd/env.sh
    source "$repo/Code/cluster/sdumont2nd/env.sh"
fi
here="$repo/Code/Fracture_fibril/slurm"
# shellcheck source=campaign_common.sh
source "$here/campaign_common.sh"

kind="${CAMPAIGN_KIND:?set CAMPAIGN_KIND=generate|fracture}"
manifest="$(campaign_root)/manifest_${kind}.tsv"
[[ -s "$manifest" ]] || { echo "missing manifest: $manifest" >&2; exit 1; }

total="$(wc -l < "$manifest")"
ntasks="${SLURM_ARRAY_TASK_COUNT:-1}"
taskid="${SLURM_ARRAY_TASK_ID:-0}"
workers="${CAMPAIGN_WORKERS:-${SLURM_CPUS_PER_TASK:-${SLURM_CPUS_ON_NODE:-8}}}"

# SHARED WORK QUEUE, not a fixed slice per task.
#
# Launch failures on this cluster are common and scale with the array size: a
# 40-task array had 29 tasks land in "launch failed requeued held" while 11 ran.
# With fixed slices those 11 tasks would only ever do their own 550 items and
# the other 1450 would wait for another round.  Instead every task walks the
# WHOLE manifest, starting at its own offset so they do not collide head-on,
# and claims each item atomically before working on it.  Any surviving subset
# of tasks therefore covers the entire manifest, and one round can finish the
# stage no matter how many tasks failed to launch.
claims="$(campaign_root)/claims/${kind}"
mkdir -p "$claims"

echo "job ........ ${SLURM_JOB_ID:-local} task ${taskid}/${ntasks}"
echo "host ....... $(hostname)"
echo "stage ...... $kind"
echo "manifest ... $manifest ($total items)"
echo "claims ..... $claims"
echo "workers .... $workers"
echo "scratch .... ${DLA_TMP}"
echo "results .... $(campaign_root)"
echo "start ...... $(date --iso-8601=seconds)"

worker="$here/worker_${kind}.sh"
[[ -x "$worker" ]] || { echo "worker not executable: $worker" >&2; exit 1; }

# One claim per item.  mkdir is atomic, so exactly one task wins each item even
# with every task reading the same manifest.  A claim only prevents duplicated
# effort; correctness never depends on it, because the workers are idempotent
# and verify their own output.
claim_and_run() {
    local key="${*// /_}"
    mkdir "$claims/$key" 2>/dev/null || return 0
    "$CAMPAIGN_WORKER" "$@" || {
        # Release the claim so a later round retries this item.
        rmdir "$claims/$key" 2>/dev/null || true
        return 1
    }
}
export -f claim_and_run
export claims CAMPAIGN_WORKER="$worker"

fields="$(head -1 "$manifest" | awk '{print NF}')"
offset=$(( taskid * 97 % (total > 0 ? total : 1) ))

# Rotate the manifest by this task's offset so tasks start in different places
# and mostly avoid contending for the same claims.
status=0
{ tail -n "+$((offset + 1))" "$manifest"; head -n "$offset" "$manifest"; } \
    | tr '\t' '\n' \
    | xargs -r -n "$fields" -P "$workers" bash -c 'claim_and_run "$@"' _ \
    || status=$?

echo "end ........ $(date --iso-8601=seconds)"
if ((status != 0)); then
    echo "WARNING: at least one item failed (xargs status $status)." >&2
    echo "Resubmit the same array to retry only what is missing." >&2
fi
exit "$status"
