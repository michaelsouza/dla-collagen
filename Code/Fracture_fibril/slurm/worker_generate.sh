#!/usr/bin/env bash
# Generate and extend ONE fibril.  Idempotent: an existing, complete extended
# file makes the worker a no-op, which is what makes the whole campaign
# resumable by resubmission.
#
#     worker_generate.sh <TS> <SEED>
#
# Kept separate from the sbatch so the logic can be exercised without Slurm.
set -euo pipefail

if (($# != 2)); then
    echo "usage: worker_generate.sh <TS> <SEED>" >&2
    exit 2
fi
ts="$1"
seed="$2"

here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=campaign_common.sh
source "$here/campaign_common.sh"

repo="${DLA_REPO:?source Code/cluster/sdumont2nd/env.sh first}"
compact_dat="$(campaign_fibril_dat "$ts" "$seed")"
extended_dat="$(campaign_extended_dat "$ts" "$seed")"
binary="${CAMPAIGN_BIN:-$(campaign_bin)}"

if [[ -s "$extended_dat" ]]; then
    exit 0
fi
if [[ ! -x "$binary" ]]; then
    echo "generator not built: $binary" >&2
    exit 1
fi

work="${DLA_TMP:-/tmp}/gen-${ts}-${seed}-$$"
mkdir -p "$work"

# On failure the log is the only evidence, and the trap is about to delete the
# scratch directory.  Keep a copy in the project area before that happens.
keep_log() {
    local dest="$(campaign_logs)/failed"
    mkdir -p "$dest" 2>/dev/null || return 0
    cp -- "$work/gen.log" "$dest/gen_ts${ts}_seed${seed}.log" 2>/dev/null || true
    echo "log kept at $dest/gen_ts${ts}_seed${seed}.log" >&2
}
trap 'rm -rf -- "$work"' EXIT

# The two binaries disagree on the default mode (fast_dla defaults to 'n',
# fast_dla2 to 's'), so -mode is always explicit.
# set -e would abort here before the diagnostics below could run, so the
# status is captured explicitly.
status=0
"$binary" \
    -ts "$ts" -mode s -num_bind "$CAMPAIGN_NUM_BIND" -seed "$seed" \
    -rng fast -jumps 1 -coverstop 1 \
    -output_dir "$work" > "$work/gen.log" 2>&1 || status=$?
if ((status != 0)); then
    echo "generator failed for ts=$ts seed=$seed (exit $status)" >&2
    tail -20 "$work/gen.log" >&2 || true
    keep_log
    exit "$status"
fi

local_dat="$work/dla_mode_s_ts_${ts}_nb_${CAMPAIGN_NUM_BIND}_seed_${seed}_.dat"
if [[ ! -s "$local_dat" ]]; then
    echo "generator produced nothing for ts=$ts seed=$seed" >&2
    tail -20 "$work/gen.log" >&2 || true
    keep_log
    exit 1
fi

# A truncated fibril is worse than a missing one: it looks valid downstream.
# The generator writes one line per molecule plus the seed rod.
molecules="$(grep -c '^uid:' "$local_dat")"
expected=$((CAMPAIGN_NUM_BIND + 1))
if ((molecules != expected)); then
    echo "ts=$ts seed=$seed: expected $expected molecules, wrote $molecules" >&2
    keep_log
    exit 1
fi

status=0
python3 -u "$repo/Code/Data_analysis/extend_fibrils_batch.py" \
    "$work" "$work/extended" >> "$work/gen.log" 2>&1 || status=$?
if ((status != 0)); then
    echo "extension failed for ts=$ts seed=$seed (exit $status)" >&2
    tail -20 "$work/gen.log" >&2 || true
    keep_log
    exit "$status"
fi

local_ext="$work/extended/ts_${ts}_seed_${seed}.dat"
if [[ ! -s "$local_ext" ]]; then
    echo "extension produced nothing for ts=$ts seed=$seed" >&2
    tail -20 "$work/gen.log" >&2 || true
    keep_log
    exit 1
fi

# Publish atomically, so an interrupted job never leaves a partial file that a
# later run would mistake for finished work.
mkdir -p "$(dirname -- "$compact_dat")" "$(dirname -- "$extended_dat")"
cp -- "$local_dat" "${compact_dat}.tmp.$$"
mv -- "${compact_dat}.tmp.$$" "$compact_dat"
cp -- "$local_ext" "${extended_dat}.tmp.$$"
mv -- "${extended_dat}.tmp.$$" "$extended_dat"

# Coverage statistics feed the Phase A record; keep them next to the logs.
mkdir -p "$(campaign_logs)/coverage"
grep -E '^(coverage|cov steps)' "$work/gen.log" \
    > "$(campaign_logs)/coverage/ts_${ts}_seed_${seed}.txt" || true
