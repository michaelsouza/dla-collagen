#!/usr/bin/env bash
# Drop claims whose work never landed, so the next round can retry them.
#
#     clear_stale_claims.sh generate|fracture [--apply]
#
# A claim is released by claim_and_run only when the WORKER fails.  When the
# TASK dies instead -- a walltime limit, a node failure, scancel -- the claim
# survives with no result behind it, and because a claim is what stops a later
# task from picking the item up, that item would be skipped by every subsequent
# round.  The campaign would then report itself short forever while doing no
# work on the very items it is short of.
#
# So between rounds, every claim is checked against the output it stands for
# and the ones with nothing complete behind them are removed.  This is safe
# only while no task of the stage is running: a claim held by a LIVE worker
# also has no result yet, and deleting it would let a second worker start the
# same item.  The guard below enforces that.
#
# Dry run by default; --apply removes.
set -euo pipefail

kind="${1:?usage: clear_stale_claims.sh generate|fracture [--apply]}"
apply=0
[[ "${2:-}" == "--apply" ]] && apply=1

here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo="${DLA_REPO:-$(cd -- "$here/../../.." && pwd)}"
if [[ -z "${DLA_PROJECT:-}" ]]; then
    # shellcheck source=../../cluster/sdumont2nd/env.sh
    source "$repo/Code/cluster/sdumont2nd/env.sh"
fi
# shellcheck source=campaign_common.sh
source "$here/campaign_common.sh"

# Refuse to run while the stage is live.  squeue lists array elements with -r;
# the job name is set by campaign.sbatch.
live="$(squeue -h -u "$USER" -r -t RUNNING,PENDING -o "%j" 2>/dev/null \
        | grep -c '^dla-campaign$' || true)"
if ((live > 0)); then
    echo "$live campaign task(s) still queued or running." >&2
    echo "Claims held by a live worker look identical to stale ones; wait." >&2
    exit 1
fi

claims="$(campaign_root)/claims/${kind}"
[[ -d "$claims" ]] || { echo "no claims directory: $claims"; exit 0; }

# NOTE on the key format: campaign.sbatch builds it as "${*// /_}", which
# substitutes inside each positional parameter and then joins them with a
# space -- so the keys contain SPACES, not underscores ("8192 109000 1").
# Read them with -printf/read rather than word splitting.
total=0; stale=0
while IFS= read -r key; do
    total=$((total + 1))
    # shellcheck disable=SC2086
    set -- $key
    case "$kind" in
    generate)  f="$(campaign_extended_dat "$1" "$2")"; ok_n=$(( (CAMPAIGN_NUM_BIND + 1) * 18 ))
               have=0; [[ -s "$f" ]] && have="$(grep -c '^uid ' "$f")"
               complete=$(( have == ok_n ? 1 : 0 )) ;;
    fracture)  f="$(campaign_result "$1" "$2" "$3")"
               have=0; [[ -s "$f" ]] && have=$(( $(grep -cE '^-+[0-9]+$' "$f" || true) + 1 ))
               complete=$(( have == CAMPAIGN_REALIZATIONS ? 1 : 0 )) ;;
    *)         echo "unknown kind: $kind" >&2; exit 2 ;;
    esac
    if ((complete == 0)); then
        stale=$((stale + 1))
        if ((apply == 1)); then
            rmdir -- "$claims/$key" 2>/dev/null || true
        else
            printf 'stale: %s\n' "$key"
        fi
    fi
done < <(find "$claims" -mindepth 1 -maxdepth 1 -printf '%f\n')

printf 'claims ..... %d\n' "$total"
printf 'stale ...... %d\n' "$stale"
if ((apply == 1)); then
    echo "removed; the next round will retry these items"
else
    echo "dry run -- pass --apply to remove"
fi
