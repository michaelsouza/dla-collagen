#!/usr/bin/env bash
# Phase 0 of the campaign plan: everything that must pass before a long job.
#
# Run it on a COMPUTE node, never on the login node:
#
#     srun --account=solverbrict --partition=cpu_amd_dev \
#          --ntasks=1 --cpus-per-task=8 --mem=16G --time=00:20:00 \
#          bash Code/cluster/sdumont2nd/validate.sh
#
# Every check is independent and reports PASS, FAIL or SKIP; the script runs
# them all and exits non-zero if any failed, so one failure does not hide the
# rest.  It writes only under $DLA_TMP and a scratch subdirectory of the
# project area.
set -uo pipefail

repo="${DLA_REPO:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)}"
export DLA_REPO="$repo"
# On the cluster this configures the module, the venv and the paths.  If the
# environment is already configured (DLA_PROJECT set), it is left alone, which
# is what lets these scripts be exercised off-cluster before submission.
if [[ -z "${DLA_PROJECT:-}" ]]; then
    # shellcheck source=env.sh
    source "$repo/Code/cluster/sdumont2nd/env.sh"
fi
# shellcheck source=../../Fracture_fibril/slurm/campaign_common.sh
source "$repo/Code/Fracture_fibril/slurm/campaign_common.sh"

PASS=0; FAIL=0; SKIP=0
report() {  # <status> <id> <message>
    printf '%-6s %-4s %s\n' "$1" "$2" "$3"
    case "$1" in PASS) ((PASS++));; FAIL) ((FAIL++));; SKIP) ((SKIP++));; esac
}

work="${DLA_TMP:-/tmp}/dla-validate-$$"
mkdir -p "$work"

# $work is node-local and vanishes with the job, so a failing check would take
# its own evidence with it -- the log the report points at would already be
# gone by the time anyone read the report.  Failures are copied to the project
# area before the trap fires.
keep="${DLA_PROJECT:-}/campaign/logs/validate"
preserve_logs() {
    [[ -n "${DLA_PROJECT:-}" ]] || return 0
    mkdir -p "$keep" 2>/dev/null || return 0
    cp -- "$work"/*.log "$keep/" 2>/dev/null || true
    echo "logs kept at $keep"
}
trap 'preserve_logs; rm -rf -- "$work"' EXIT

echo "repo ....... $repo"
echo "host ....... $(hostname)"
echo "scratch .... $work"
echo "project .... ${DLA_PROJECT:-unset}"
echo

# --- V0: environment -------------------------------------------------------
if python3 - <<'PY' > "$work/v0.log" 2>&1
import numpy, scipy, pandas, matplotlib, tqdm, sklearn, mpmath, duckdb, pytest, sys
assert sys.version_info[:2] >= (3, 12), sys.version
PY
then report PASS V0 "environment: python $(python3 -c 'import sys;print(".".join(map(str,sys.version_info[:3])))'), all imports"
else report FAIL V0 "environment: see $work/v0.log"; fi

# --- V1: builds ------------------------------------------------------------
# Two builds on purpose.  Production uses -O3 -march=native; the identity check
# in V3 needs a build whose floating-point behaviour matches the reference,
# because -march=native enables FMA contraction in launch_on_sphere, the one
# floating-point step of the generator, where a 1-ULP change can move an
# integer lattice coordinate.
mkdir -p "$work/bin"
if g++ -std=c++17 -O2 -Wall -Wextra \
       -o "$work/bin/fast_dla" "$repo/Code/Dla/fast_dla.cpp" 2> "$work/v1a.log" \
   && g++ -std=c++17 -O2 -Wall -Wextra \
       -o "$work/bin/fast_dla2_o2" "$repo/Code/Dla/fast_dla2.cpp" 2>> "$work/v1a.log"
then report PASS V1a "reference builds (-O2)"
else report FAIL V1a "reference builds: see $work/v1a.log"; fi

if g++ -std=c++17 -O3 -march=native -Wall -Wextra \
       -o "$work/bin/fast_dla2" "$repo/Code/Dla/fast_dla2.cpp" 2> "$work/v1b.log"
then report PASS V1b "production build (-O3 -march=native)"
else report FAIL V1b "production build: see $work/v1b.log"; fi

# --- V2: test suites -------------------------------------------------------
# Both suites run FROM THE REPOSITORY ROOT.  Five modules in Code/Data_analysis
# import `from Code.Data_analysis...`, which needs the root on sys.path; running
# pytest from inside the directory fails collection before any test executes.
if (cd "$repo" && python3 -m pytest -q Code/Fracture_fibril > "$work/v2a.log" 2>&1)
then report PASS V2a "Code/Fracture_fibril suite ($(grep -oE '[0-9]+ passed' "$work/v2a.log" | head -1))"
else report FAIL V2a "Code/Fracture_fibril suite: see v2a.log"; fi

if (cd "$repo" && python3 -m pytest -q Code/Data_analysis > "$work/v2b.log" 2>&1)
then report PASS V2b "Code/Data_analysis suite ($(grep -oE '[0-9]+ passed' "$work/v2b.log" | head -1))"
else report FAIL V2b "Code/Data_analysis suite: see v2b.log"; fi

# --- V3: bit-identity, fast_dla2 default mode vs fast_dla ------------------
# Covers both cost regimes: bulk diffusion dominates at low T_s, surface
# diffusion at high T_s.
identity_ok=1
for ts in 2 64; do
    for d in a b; do mkdir -p "$work/id$d"; done
    "$work/bin/fast_dla"     -ts "$ts" -mode s -num_bind 400 -seed 42 \
        -output_dir "$work/ida" > /dev/null 2>&1
    "$work/bin/fast_dla2_o2" -ts "$ts" -mode s -num_bind 400 -seed 42 \
        -output_dir "$work/idb" > /dev/null 2>&1
    f="dla_mode_s_ts_${ts}_nb_400_seed_42_.dat"
    if ! cmp -s "$work/ida/$f" "$work/idb/$f"; then
        identity_ok=0
        report FAIL V3 "ts=$ts: fast_dla2 default mode differs from fast_dla"
    fi
done
((identity_ok == 1)) && report PASS V3 "bit-identity at ts=2 and ts=64"

# --- V4: accelerators ------------------------------------------------------
# -coverstop is an exact optimisation of the placement, so with the SAME rng
# and jump settings the fibril must be unchanged whenever every molecule
# reached coverage.  Below full coverage the streams legitimately diverge, so
# this reports the coverage fraction rather than asserting identity.
mkdir -p "$work/cov"
cov_out="$("$work/bin/fast_dla2" -ts 8192 -mode s -num_bind 1500 -seed 91 \
    -rng fast -jumps 1 -coverstop 1 -output_dir "$work/cov" 2>&1 \
    | grep -E '^coverage' || true)"
if [[ -n "$cov_out" ]]; then
    report PASS V4 "coverage instrumentation live: $cov_out"
else
    report FAIL V4 "coverage instrumentation produced no report"
fi

# --- V5/V6: end-to-end micro-campaign -------------------------------------
# Two conditions, two fibrils each, five realizations: generation, extension,
# quenched fracture, and the strict parser, with no manual step in between.
# The micro-campaign gets a throwaway project root, but the log destination
# resolved above still points at the real one.
export DLA_PROJECT="$work/project"
export CAMPAIGN_NUM_BIND=1500
export CAMPAIGN_REALIZATIONS=5
export CAMPAIGN_BIN="$work/bin/fast_dla2"
slurm_dir="$repo/Code/Fracture_fibril/slurm"

micro_ok=1
for spec in "128 0" "8192 0"; do
    read -r ts k <<< "$spec"
    i="$(campaign_ts_index "$ts")" || { micro_ok=0; break; }
    seed="$(campaign_seed "$i" "$k")"
    if ! bash "$slurm_dir/worker_generate.sh" "$ts" "$seed" > "$work/v5_gen_${ts}.log" 2>&1; then
        micro_ok=0
        report FAIL V5 "generation failed for ts=$ts: see $work/v5_gen_${ts}.log"
        continue
    fi
    if ! bash "$slurm_dir/worker_fracture.sh" "$ts" "$seed" 2 > "$work/v5_frac_${ts}.log" 2>&1; then
        micro_ok=0
        report FAIL V5 "fracture failed for ts=$ts: see $work/v5_frac_${ts}.log"
    fi
done
((micro_ok == 1)) && report PASS V5 "end-to-end generate + extend + fracture"

# The parser is the most protocol-coupled component in the chain: it pins the
# header, the filename convention and six per-row invariants.
if ((micro_ok == 1)) && python3 -u "$repo/Code/Data_analysis/read_avalanche_runs.py" \
        summary "$(campaign_runs)" > "$work/v6.log" 2>&1; then
    realizations="$(python3 -c "import json;print(json.load(open('$work/v6.log'))['totals']['realizations'])" 2>/dev/null || echo '?')"
    report PASS V6 "read_avalanche_runs accepts the output ($realizations realizations)"
else
    report FAIL V6 "parser rejected the output: see $work/v6.log"
fi

# --- V7: cost, to size the array ------------------------------------------
if ((micro_ok == 1)); then
    i="$(campaign_ts_index 128)"; seed="$(campaign_seed "$i" 1)"
    t0=$(date +%s)
    bash "$slurm_dir/worker_generate.sh" 128 "$seed" > /dev/null 2>&1
    t1=$(date +%s)
    bash "$slurm_dir/worker_fracture.sh" 128 "$seed" 2 > /dev/null 2>&1
    t2=$(date +%s)
    report PASS V7 "cost at nb=$CAMPAIGN_NUM_BIND: generate $((t1-t0))s, fracture $((t2-t1))s for $CAMPAIGN_REALIZATIONS realizations"
else
    report SKIP V7 "cost measurement skipped: micro-campaign failed"
fi

# --- V8: storage -----------------------------------------------------------
# The group quota is the one that binds: results live in the 6 TB project area,
# not in the 100 GB home.
if quota="$(lfs quota -h -g solverbrict /petrobr 2>/dev/null | tail -2)"; then
    report PASS V8 "group quota: $(echo "$quota" | tr '\n' ' ')"
else
    report SKIP V8 "lfs quota unavailable (not on the cluster?)"
fi

echo
printf 'passed %d, failed %d, skipped %d\n' "$PASS" "$FAIL" "$SKIP"
((FAIL == 0)) || exit 1
