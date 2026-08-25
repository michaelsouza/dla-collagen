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

# Contiguous slice, ceiling division so the last task absorbs the remainder.
per=$(( (total + ntasks - 1) / ntasks ))
first=$(( taskid * per + 1 ))
last=$(( first + per - 1 ))
((last > total)) && last=$total

echo "job ........ ${SLURM_JOB_ID:-local} task ${taskid}/${ntasks}"
echo "host ....... $(hostname)"
echo "stage ...... $kind"
echo "manifest ... $manifest ($total items)"
echo "slice ...... lines $first..$last"
echo "workers .... $workers"
echo "scratch .... ${DLA_TMP}"
echo "results .... $(campaign_root)"
echo "start ...... $(date --iso-8601=seconds)"

((first > last)) && { echo "empty slice; nothing to do"; exit 0; }

worker="$here/worker_${kind}.sh"
[[ -x "$worker" ]] || { echo "worker not executable: $worker" >&2; exit 1; }

# xargs returns 123 if any invocation failed.  Failures are reported but do not
# abort the slice: one bad fibril should not discard the rest of the task, and
# resubmitting picks up exactly what is missing.
status=0
sed -n "${first},${last}p" "$manifest" \
    | tr '\t' '\n' \
    | xargs -r -n "$(head -1 "$manifest" | awk '{print NF}')" -P "$workers" "$worker" \
    || status=$?

echo "end ........ $(date --iso-8601=seconds)"
if ((status != 0)); then
    echo "WARNING: at least one item failed (xargs status $status)." >&2
    echo "Resubmit the same array to retry only what is missing." >&2
fi
exit "$status"
