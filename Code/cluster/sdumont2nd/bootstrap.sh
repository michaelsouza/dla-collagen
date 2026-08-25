#!/usr/bin/env bash
# Build the project environment on SDumont2 from scratch. Run once per
# account; re-running it is safe and only re-installs the extra packages.
#
#     bash Code/cluster/sdumont2nd/bootstrap.sh
#
set -euo pipefail

if ! command -v module >/dev/null 2>&1; then
    # shellcheck disable=SC1090
    source /etc/profile.d/*modules*.sh 2>/dev/null || true
fi
module load anaconda3/2024.10

DLA_VENV="${DLA_VENV:-$HOME/envs/dla-collagen}"

# The venv lives outside the work tree: a Lustre home makes every git
# operation walk whatever sits under the repository, and a venv adds
# thousands of small files to that walk.
if [ ! -f "$DLA_VENV/bin/activate" ]; then
    mkdir -p "$(dirname "$DLA_VENV")"
    python -m venv --system-site-packages "$DLA_VENV"
    echo "created venv at $DLA_VENV"
else
    echo "reusing venv at $DLA_VENV"
fi

# shellcheck disable=SC1091
source "$DLA_VENV/bin/activate"
python -m pip install --upgrade pip

# The anaconda3 module already satisfies every entry in requirements.txt
# except duckdb. pytest is added for the test suite.
python -m pip install duckdb pytest

python - <<'PY'
import sys
print("python", sys.version.split()[0], sys.executable)
for m in ["numpy", "scipy", "pandas", "matplotlib", "tqdm",
          "sklearn", "mpmath", "duckdb", "pytest"]:
    try:
        mod = __import__(m)
        print("  %-12s %s" % (m, getattr(mod, "__version__", "ok")))
    except Exception as exc:  # noqa: BLE001
        print("  %-12s MISSING: %s" % (m, exc))
        sys.exit(1)
PY

echo
echo "done -- from now on use: source Code/cluster/sdumont2nd/env.sh"
