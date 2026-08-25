#!/usr/bin/env bash
# Verify a campaign stage against its manifest, by CONTENT.
#
#     check_campaign.sh generate
#     check_campaign.sh fracture
#
# A job array can finish with a slice never executed -- a task that hits
# "launch failed requeued held" stays held, produces no log, and the array
# still reports done.  Existence of a file is not evidence either: an
# interrupted worker can leave a short one.  So every item is checked against
# what it should contain, and the missing ones are listed.
set -euo pipefail

kind="${1:?usage: check_campaign.sh generate|fracture}"
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo="${DLA_REPO:-$(cd -- "$here/../../.." && pwd)}"
if [[ -z "${DLA_PROJECT:-}" ]]; then
    # shellcheck source=../../cluster/sdumont2nd/env.sh
    source "$repo/Code/cluster/sdumont2nd/env.sh"
fi
# shellcheck source=campaign_common.sh
source "$here/campaign_common.sh"

manifest="$(campaign_root)/manifest_${kind}.tsv"
[[ -s "$manifest" ]] || { echo "missing manifest: $manifest" >&2; exit 1; }

# Counters are incremented with arithmetic ASSIGNMENT, never ((x++)):
# post-increment evaluates to the OLD value, so ((x++)) with x=0 returns exit
# status 1 and set -e aborts the loop on its first iteration.
total=0; ok=0; missing=0; short=0
missing_list="$(mktemp)"
trap 'rm -f -- "$missing_list"' EXIT

while IFS=$'\t' read -r a b c; do
    total=$((total + 1))
    case "$kind" in
    generate)
        f="$(campaign_extended_dat "$a" "$b")"
        want=$(( (CAMPAIGN_NUM_BIND + 1) * 18 ))
        if [[ ! -s "$f" ]]; then
            missing=$((missing + 1)); printf '%s\t%s\n' "$a" "$b" >> "$missing_list"
        elif (( $(grep -c '^uid ' "$f") != want )); then
            short=$((short + 1)); printf '%s\t%s\tSHORT\n' "$a" "$b" >> "$missing_list"
        else
            ok=$((ok + 1))
        fi
        ;;
    fracture)
        f="$(campaign_result "$a" "$b" "$c")"
        if [[ ! -s "$f" ]]; then
            missing=$((missing + 1)); printf '%s\t%s\t%s\n' "$a" "$b" "$c" >> "$missing_list"
        else
            n=$(( $(grep -cE '^-+[0-9]+$' "$f" || true) + 1 ))
            if (( n != CAMPAIGN_REALIZATIONS )); then
                short=$((short + 1))
                printf '%s\t%s\t%s\tSHORT(%d/%d)\n' \
                    "$a" "$b" "$c" "$n" "$CAMPAIGN_REALIZATIONS" >> "$missing_list"
            else
                ok=$((ok + 1))
            fi
        fi
        ;;
    *)
        echo "unknown kind: $kind" >&2; exit 2 ;;
    esac
done < "$manifest"

printf 'stage ...... %s\n' "$kind"
printf 'manifest ... %s\n' "$manifest"
printf 'complete ... %d/%d\n' "$ok" "$total"
printf 'missing .... %d\n' "$missing"
printf 'short ...... %d\n' "$short"

if (( missing + short > 0 )); then
    echo
    echo "first 20 incomplete items:"
    head -20 "$missing_list"
    echo
    echo "Resubmit the same array: the workers are idempotent and will do only"
    echo "these.  If a task shows 'launch failed requeued held', release it with"
    echo "scontrol release <JOBID>_<TASK>."
    exit 1
fi
echo "stage complete"
