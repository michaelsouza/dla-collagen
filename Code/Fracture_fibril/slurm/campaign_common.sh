#!/usr/bin/env bash
# Shared definitions for the quenched campaign on SDumont2.
#
# Source it -- do not execute it.  Every script in this directory sources this
# file so the grid, the seed scheme and the directory layout are defined once.

# --- grid ------------------------------------------------------------------
# Phase A measured the surface-diffusion coverage of every condition and found
# none of them saturated (82.9% at T_s=8192, less below), so no condition can
# be dropped: all ten remain distinct.  See Reviews/PhaseA_ts_saturation/.
CAMPAIGN_TS=(2 8 16 32 64 128 512 1024 4096 8192)

# Weibull moduli.  Parkinson et al. (1997) swept five values and derived
# physics from the sweep; Referee 1 comment 3 asks for the same.
CAMPAIGN_M=(1 2 3 5 10)
# The Phase B pilot fixes m=2 and only wants the variance structure, so the
# sweep is overridable: CAMPAIGN_M_CSV=2
if [[ -n "${CAMPAIGN_M_CSV:-}" ]]; then
    IFS=',' read -r -a CAMPAIGN_M <<< "$CAMPAIGN_M_CSV"
fi

CAMPAIGN_NUM_BIND="${CAMPAIGN_NUM_BIND:-30000}"
CAMPAIGN_FIBRILS="${CAMPAIGN_FIBRILS:-200}"      # ceiling; Phase B may stop earlier
# The Phase B pilot (10 T_s x 20 fibrils x 50 realizations, m=2) measured an
# ICC of 0.19-0.35, so the within-fibril term stops dominating the variance well
# before 100 realizations while the fixed-budget argument still forbids 1.  See
# Reviews/decision_log/2026-08-25_faseB_tamanhos_campanha.md. 100 was a placeholder.
CAMPAIGN_REALIZATIONS="${CAMPAIGN_REALIZATIONS:-50}"

# --- seeds -----------------------------------------------------------------
# seed = 100000 + 1000*i + k, with i the index of T_s in CAMPAIGN_TS and k the
# fibril index.  The block per condition matters: Phase B stops each condition
# independently, so extending one T_s must not disturb the seeds of another.
# Nothing historical reaches 100000 (the old campaign tops out near 10750).
campaign_seed() {   # <ts_index> <fibril_index>
    printf '%d' $(( 100000 + 1000 * $1 + $2 ))
}

campaign_ts_index() {   # <ts>
    local i
    for i in "${!CAMPAIGN_TS[@]}"; do
        if [[ "${CAMPAIGN_TS[$i]}" == "$1" ]]; then
            printf '%d' "$i"
            return 0
        fi
    done
    echo "unknown T_s: $1" >&2
    return 1
}

# --- layout ----------------------------------------------------------------
# $DLA_PROJECT is exported by Code/cluster/sdumont2nd/env.sh and resolves to the
# 6 TB project area.  $HOME carries only a 100 GB quota and holds the clone and
# the venv, never simulation output.
# CAMPAIGN_NAME keeps the Phase B pilot in its own tree, so a pilot run can
# never be mistaken for production data or block it by occupying its paths.
campaign_root()     { printf '%s/%s' "${DLA_PROJECT:?source Code/cluster/sdumont2nd/env.sh first}" "${CAMPAIGN_NAME:-campaign}"; }
campaign_compact()  { printf '%s/fibrils/compact' "$(campaign_root)"; }
campaign_extended() { printf '%s/fibrils/extended' "$(campaign_root)"; }
campaign_runs()     { printf '%s/avalanches/runs' "$(campaign_root)"; }
campaign_logs()     { printf '%s/logs' "$(campaign_root)"; }

campaign_fibril_dat() {   # <ts> <seed>
    printf '%s/dla_mode_s_ts_%s_nb_%s_seed_%s_.dat' \
        "$(campaign_compact)" "$1" "$CAMPAIGN_NUM_BIND" "$2"
}
campaign_extended_dat() { # <ts> <seed>
    printf '%s/ts_%s_seed_%s.dat' "$(campaign_extended)" "$1" "$2"
}
campaign_result() {       # <ts> <seed> <m>
    printf '%s/ts_%s/ts_%s_seed_%s_m_%s.txt' "$(campaign_runs)" "$1" "$1" "$2" "$3"
}

# --- binaries --------------------------------------------------------------
# Built by the validation battery.  -O3 -march=native is the production build;
# the bit-identity check uses a separate -O2 build, because -march=native
# enables FMA contraction in the one floating-point step of the generator
# (launch_on_sphere) and a 1-ULP change there can move an integer coordinate.
campaign_bin() { printf '%s/bin/fast_dla2' "$(campaign_root)"; }
