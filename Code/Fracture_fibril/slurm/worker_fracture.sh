#!/usr/bin/env bash
# Run the quenched fiber-bundle protocol on ONE fibril at ONE Weibull modulus.
# Idempotent, like worker_generate.sh: a complete result makes it a no-op.
#
#     worker_fracture.sh <TS> <SEED> <M>
set -euo pipefail

if (($# != 3)); then
    echo "usage: worker_fracture.sh <TS> <SEED> <M>" >&2
    exit 2
fi
ts="$1"
seed="$2"
m="$3"

here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=campaign_common.sh
source "$here/campaign_common.sh"

repo="${DLA_REPO:?source Code/cluster/sdumont2nd/env.sh first}"
extended_dat="$(campaign_extended_dat "$ts" "$seed")"
result="$(campaign_result "$ts" "$seed" "$m")"
reps="$CAMPAIGN_REALIZATIONS"

if [[ ! -s "$extended_dat" ]]; then
    echo "missing input: $extended_dat" >&2
    exit 1
fi

# Resume by counting realization separators, the same convention
# resume_parallel.sh uses: realizations = separators + 1.
done_reps=0
if [[ -s "$result" ]]; then
    done_reps=$(( $(grep -cE '^-+[0-9]+$' "$result" || true) + 1 ))
    if ((done_reps >= reps)); then
        exit 0
    fi
fi

work="${DLA_TMP:-/tmp}/frac-${ts}-${seed}-${m}-$$"
mkdir -p "$work"

keep_log() {
    local dest="$(campaign_logs)/failed"
    mkdir -p "$dest" 2>/dev/null || return 0
    cp -- "$work/frac.log" "$dest/frac_ts${ts}_seed${seed}_m${m}.log" 2>/dev/null || true
    echo "log kept at $dest/frac_ts${ts}_seed${seed}_m${m}.log" >&2
}
trap 'rm -rf -- "$work"' EXIT

# Copy the input to node-local storage: the simulation is chatty on I/O and
# Lustre is not the place for it.  The .db cache is rebuilt beside it.
cp -- "$extended_dat" "$work/"
local_dat="$work/$(basename -- "$extended_dat")"

# A partial result is carried in so the run appends to it rather than
# restarting from realization zero.
legacy_dir="$work/out"
mkdir -p "$legacy_dir/ts_${ts}"
if ((done_reps > 0)); then
    cp -- "$result" "$legacy_dir/ts_${ts}/$(basename -- "$result")"
fi

# The RNG seed is derived from the fibril seed and the modulus, so every
# (fibril, m) pair draws an independent set of quenched thresholds while the
# whole campaign stays reproducible from the manifest alone.
rng_seed=$(( seed * 977 + m ))

# set -e would abort here before the diagnostics below could run.
status=0
python3 -u "$repo/Code/Fracture_fibril/fiber_bundle_ava.py" \
    -file "$local_dat" -n "$reps" -m "$m" -seed "$rng_seed" \
    -start "$done_reps" -legacy-dir "$legacy_dir" > "$work/frac.log" 2>&1 || status=$?
if ((status != 0)); then
    echo "fracture failed for ts=$ts seed=$seed m=$m (exit $status)" >&2
    tail -20 "$work/frac.log" >&2 || true
    keep_log
    exit "$status"
fi

local_result="$legacy_dir/ts_${ts}/$(basename -- "$result")"
if [[ ! -s "$local_result" ]]; then
    echo "fracture produced nothing for ts=$ts seed=$seed m=$m" >&2
    tail -20 "$work/frac.log" >&2 || true
    keep_log
    exit 1
fi

written=$(( $(grep -cE '^-+[0-9]+$' "$local_result" || true) + 1 ))
if ((written != reps)); then
    echo "ts=$ts seed=$seed m=$m: expected $reps realizations, wrote $written" >&2
    keep_log
    exit 1
fi

mkdir -p "$(dirname -- "$result")"
cp -- "$local_result" "${result}.tmp.$$"
mv -- "${result}.tmp.$$" "$result"
