#!/usr/bin/env bash
# Submit one campaign stage.  Extra flags pass through to sbatch.
#
#     CAMPAIGN_KIND=generate ./submit_campaign.sh
#     CAMPAIGN_KIND=fracture ./submit_campaign.sh --time=48:00:00
set -euo pipefail

here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo="${DLA_REPO:-$(cd -- "$here/../../.." && pwd)}"
# On the cluster this configures the module, the venv and the paths.  If the
# environment is already configured (DLA_PROJECT set), it is left alone, which
# is what lets these scripts be exercised off-cluster before submission.
if [[ -z "${DLA_PROJECT:-}" ]]; then
    # shellcheck source=../../cluster/sdumont2nd/env.sh
    source "$repo/Code/cluster/sdumont2nd/env.sh"
fi
# shellcheck source=campaign_common.sh
source "$here/campaign_common.sh"

kind="${CAMPAIGN_KIND:?set CAMPAIGN_KIND=generate|fracture}"
manifest="$(campaign_root)/manifest_${kind}.tsv"
[[ -s "$manifest" ]] || {
    echo "missing manifest: $manifest" >&2
    echo "run: $here/make_manifest.sh $kind" >&2
    exit 1
}

# The CPU ceiling is 1920 and the job ceiling is 100, but cpu_amd is shared and
# usually has no idle node, so what actually decides start time is how easily a
# task backfills.  Forty tasks of 48 cores reach the CPU ceiling while each one
# fits in the spare cores of a partially used node; ten exclusive nodes would
# queue behind everyone else.
tasks="${CAMPAIGN_TASKS:-40}"
cpus="${CAMPAIGN_CPUS:-48}"

# Ask for the memory we actually use.  DefMemPerCPU on cpu_amd is 7800 MB, so a
# 48-core task would silently reserve 374 GB; measured MaxRSS for a 24-process
# generation task is 0.56 GB, about 23 MB per process.  Over-reserving is not
# free on a shared cluster: a 1.5 TB node would fit only four default-memory
# tasks, so memory, not cores, becomes the packing constraint and other users
# are locked out of cores that sit idle.  2 GB per core leaves a wide margin
# over the fracture protocol's few hundred MB per process.
mem_per_cpu="${CAMPAIGN_MEM_PER_CPU:-2G}"
concurrent="${CAMPAIGN_CONCURRENT:-$tasks}"
if ((concurrent > 100)); then
    echo "QOS allows at most 100 running jobs; capping." >&2
    concurrent=100
fi

mkdir -p "$(campaign_root)/logs" logs

# MaxSubmitPU=100 counts EVERY array element, across all of your jobs, queued or
# running.  %N throttling does not help: it limits concurrency, not submission.
# So the budget is 100 minus whatever is already in the queue -- a single held
# task left over from an earlier attempt is enough to make a 100-task array
# bounce.
in_queue="$(squeue -h -u "$USER" -r 2>/dev/null | wc -l || echo 0)"
limit="$(sacctmgr -nP show qos ict_cpu-genoa format=MaxSubmitJobsPU 2>/dev/null \
         | tr -d '|' | head -1)"
limit="${limit:-100}"
if (( in_queue + tasks > limit )); then
    echo "submit budget: $in_queue already queued + $tasks requested > $limit" >&2
    echo "Drain the queue or lower CAMPAIGN_TASKS.  Held tasks count too:" >&2
    squeue -h -u "$USER" -r -o "  %.12i %.8T %R" | head -10 >&2
    exit 1
fi

echo "stage ...... $kind"
echo "submitted .. $in_queue in queue, limit $limit"
echo "items ...... $(wc -l < "$manifest")"
echo "array ...... 0-$((tasks - 1))%${concurrent}"
echo "cpus/task .. $cpus"
echo "mem/cpu .... $mem_per_cpu"
echo "account .... $DLA_ACCOUNT"
echo "partition .. ${DLA_PARTITION}"

# --test-only validates against the live QOS without consuming the budget; it
# is the cheapest way to find out that a batch would be rejected.
if ! sbatch --test-only \
        --account="$DLA_ACCOUNT" --partition="$DLA_PARTITION" \
        --array="0-$((tasks - 1))%${concurrent}" --cpus-per-task="$cpus" \
        --mem-per-cpu="$mem_per_cpu" \
        "$@" "$here/campaign.sbatch" 2>&1 | tee /dev/stderr | grep -q "to start at"; then
    echo "dry run rejected; not submitting" >&2
    exit 1
fi

sbatch \
    --account="$DLA_ACCOUNT" \
    --partition="$DLA_PARTITION" \
    --array="0-$((tasks - 1))%${concurrent}" \
    --cpus-per-task="$cpus" \
    --mem-per-cpu="$mem_per_cpu" \
    --export=ALL,CAMPAIGN_KIND="$kind",DLA_REPO="$repo" \
    "$@" \
    "$here/campaign.sbatch"
