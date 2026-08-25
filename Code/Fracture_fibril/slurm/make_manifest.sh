#!/usr/bin/env bash
# Build the campaign work lists.
#
#     make_manifest.sh generate [FIBRILS]      -> one line per fibril:  TS SEED
#     make_manifest.sh fracture [FIBRILS]      -> one line per run:     TS SEED M
#
# Written to $DLA_PROJECT/campaign/manifest_<kind>.tsv.  The array jobs slice
# these; nothing else defines the work.
set -euo pipefail

kind="${1:?usage: make_manifest.sh generate|fracture [FIBRILS]}"
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=campaign_common.sh
source "$here/campaign_common.sh"

fibrils="${2:-$CAMPAIGN_FIBRILS}"
root="$(campaign_root)"
mkdir -p "$root"
out="$root/manifest_${kind}.tsv"
tmp="$out.tmp.$$"
: > "$tmp"

case "$kind" in
generate)
    for i in "${!CAMPAIGN_TS[@]}"; do
        ts="${CAMPAIGN_TS[$i]}"
        for ((k = 0; k < fibrils; k++)); do
            printf '%s\t%s\n' "$ts" "$(campaign_seed "$i" "$k")" >> "$tmp"
        done
    done
    ;;
fracture)
    # Descending T_s: the expensive conditions dispatch first, so the tail of
    # the campaign is cheap work rather than a single long straggler.
    for ((i = ${#CAMPAIGN_TS[@]} - 1; i >= 0; i--)); do
        ts="${CAMPAIGN_TS[$i]}"
        for m in "${CAMPAIGN_M[@]}"; do
            for ((k = 0; k < fibrils; k++)); do
                printf '%s\t%s\t%s\n' "$ts" "$(campaign_seed "$i" "$k")" "$m" >> "$tmp"
            done
        done
    done
    ;;
*)
    echo "unknown manifest kind: $kind" >&2
    exit 2
    ;;
esac

mv -- "$tmp" "$out"
printf 'manifest: %s\nitems:    %s\n' "$out" "$(wc -l < "$out")"
