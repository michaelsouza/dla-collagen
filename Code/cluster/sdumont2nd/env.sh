#!/usr/bin/env bash
# Canonical environment for this repository on SDumont2 (LNCC).
#
# Source it -- do not execute it:
#
#     source Code/cluster/sdumont2nd/env.sh
#
# It is idempotent and safe to source from a login shell, from an `srun`
# session, and from inside an sbatch script.

# --- module + interpreter -------------------------------------------------
# The cluster ships Python 3.9 in /usr/bin; the project needs 3.12. The
# anaconda3 module already provides every requirements.txt entry except
# duckdb, so the venv sits on top of it with --system-site-packages and
# adds only duckdb and pytest.
if ! command -v module >/dev/null 2>&1; then
    # shellcheck disable=SC1090
    source /etc/profile.d/*modules*.sh 2>/dev/null || true
fi
module load anaconda3/2024.10

DLA_VENV="${DLA_VENV:-$HOME/envs/dla-collagen}"
if [ ! -f "$DLA_VENV/bin/activate" ]; then
    echo "venv not found at $DLA_VENV -- run Code/cluster/sdumont2nd/bootstrap.sh first" >&2
    return 1 2>/dev/null || exit 1
fi
# shellcheck disable=SC1091
source "$DLA_VENV/bin/activate"

# --- one core per task ----------------------------------------------------
# Every batch task in this project is single-core. numpy here is linked
# against MKL, which on these AMD Genoa nodes would otherwise spawn threads
# the cpuset does not grant and oversubscribe the core.
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-1}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
export NUMEXPR_NUM_THREADS="${NUMEXPR_NUM_THREADS:-1}"

# Compute nodes have no display; keep matplotlib headless.
export MPLBACKEND="${MPLBACKEND:-Agg}"

# --- SLURM defaults -------------------------------------------------------
export DLA_ACCOUNT="${DLA_ACCOUNT:-solverbrict}"
export DLA_PARTITION="${DLA_PARTITION:-cpu_amd}"
export DLA_PARTITION_DEV="${DLA_PARTITION_DEV:-cpu_amd_dev}"

# --- repository root ------------------------------------------------------
export DLA_REPO="${DLA_REPO:-$HOME/gitrepos/dla-collagen}"

# SLURM_TMPDIR does not exist on SDumont2; TMPDIR points at node-local /tmp.
export DLA_SCRATCH="${SLURM_TMPDIR:-${TMPDIR:-/tmp}}"
