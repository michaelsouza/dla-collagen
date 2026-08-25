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

# Ten wide tasks saturate the 1920-CPU ceiling using a tenth of the 100-job
# allowance.  Raising this past 10 buys nothing: the CPU cap binds first.
tasks="${CAMPAIGN_TASKS:-10}"
concurrent="${CAMPAIGN_CONCURRENT:-$tasks}"
if ((concurrent > 100)); then
    echo "QOS allows at most 100 running jobs; capping." >&2
    concurrent=100
fi

mkdir -p "$(campaign_root)/logs" logs

echo "stage ...... $kind"
echo "items ...... $(wc -l < "$manifest")"
echo "array ...... 0-$((tasks - 1))%${concurrent}"
echo "account .... $DLA_ACCOUNT"
echo "partition .. ${DLA_PARTITION}"

sbatch \
    --account="$DLA_ACCOUNT" \
    --partition="$DLA_PARTITION" \
    --array="0-$((tasks - 1))%${concurrent}" \
    --export=ALL,CAMPAIGN_KIND="$kind",DLA_REPO="$repo" \
    "$@" \
    "$here/campaign.sbatch"
