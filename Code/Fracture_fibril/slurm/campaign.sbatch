#!/usr/bin/env bash
# Quenched campaign on SDumont2.  One script drives both stages; the stage is
# chosen with CAMPAIGN_KIND=generate|fracture.
#
#     source Code/cluster/sdumont2nd/env.sh
#     Code/Fracture_fibril/slurm/make_manifest.sh generate
#     CAMPAIGN_KIND=generate Code/Fracture_fibril/slurm/submit_campaign.sh
#
# Shape: few wide tasks rather than many single-core ones.  The QOS caps the
# account at 1920 CPUs AND at 100 running jobs, so ten 192-core tasks saturate
# the CPU ceiling while using a tenth of the job slots.  Each task takes a
# contiguous slice of the manifest and runs it with xargs -P (GNU parallel is
# not assumed to exist).

#SBATCH --job-name=dla-campaign
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --time=24:00:00
#SBATCH --output=logs/%x-%A_%a.out
#SBATCH --error=logs/%x-%A_%a.err

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
workers="${CAMPAIGN_WORKERS:-${SLURM_CPUS_ON_NODE:-8}}"

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
