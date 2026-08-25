# Running on SDumont2 (LNCC)

SDumont2 is the cluster used for the production runs of this repository. All
figures below were measured on the cluster in August 2026; re-check them with
the commands given in each section before relying on them.

## Access

The login alias is configured in the local `~/.ssh/config`:

```bash
ssh sdumont2nd
```

The work tree on the cluster is a normal clone of `michaelsouza/dla-collagen`:

```text
$HOME/gitrepos/dla-collagen
```

`$HOME` resolves to `/petrobr/parceirosbr/home/<user>`. Code moves between the
laptop and the cluster **through git only** — never by copying a working tree.
The cluster holds its own passphrase-less SSH key (`~/.ssh/id_ed25519_github`,
pinned with `IdentitiesOnly yes`), so `git pull` and `git push` work from a
login shell and from inside a batch job.

## Account, partitions, and limits

```bash
sacctmgr -nP show assoc user="$USER" format=Account,Partition,QOS
sacctmgr -nP show qos ict_cpu-genoa format=Name,MaxWall,MaxTRESPU,MaxJobsPU,MaxSubmitJobsPU
```

- Account: `solverbrict`.
- Production CPU partition: `cpu_amd` — 20 nodes, 192 cores each (2 x 96-core
  AMD Genoa, `ThreadsPerCore=1`), 1.5 TB RAM per node, no wall-clock limit.
- Development partition: `cpu_amd_dev` — same nodes, 20-minute limit. Use it
  for every smoke test and benchmark.
- GPU partitions exist under the same account (`ict-h100`, `ict-gh200`,
  `ict-mi300a`) but nothing in this repository uses a GPU.

QOS `ict_cpu-genoa` caps the account at **1920 CPUs**, **100 running jobs**,
and **300 submitted jobs** per user; `MaxArraySize` is 1001. An array of 300
tasks therefore fills the submit quota exactly and must be throttled to at most
`%100` concurrent tasks. `Code/Fracture_fibril/slurm/run_array.sbatch` was
written for a different cluster and still says `%150` — lower it before
submitting here.

## Environment

Do not build a fresh conda environment. The `anaconda3/2024.10` module already
provides Python 3.12.7 and every package in `requirements.txt` (numpy 1.26.4,
scipy 1.13.1, pandas 2.2.2, matplotlib 3.9.2, tqdm 4.66.5, scikit-learn 1.5.1,
mpmath 1.3.0). The project venv sits on top of it with `--system-site-packages`
and adds only what the module lacks: `duckdb` and `pytest`.

The venv lives at `~/envs/dla-collagen`, **outside** the work tree. The home
directory is Lustre, where thousands of small files make every git operation
and every metadata-heavy command markedly slower.

One-time setup:

```bash
bash Code/cluster/sdumont2nd/bootstrap.sh
```

Every session, and at the top of every job script:

```bash
source Code/cluster/sdumont2nd/env.sh
```

`env.sh` loads the module, activates the venv, pins all BLAS/OpenMP thread
counts to 1, sets `MPLBACKEND=Agg`, and exports `DLA_ACCOUNT`,
`DLA_PARTITION`, `DLA_PARTITION_DEV`, `DLA_REPO`, and `DLA_SCRATCH`. It is
idempotent and safe to source more than once.

numpy on this module is linked against MKL, running on AMD hardware. Since
every task in this project is single-core, pinning the thread counts to 1 —
which `env.sh` does — removes the question entirely. Revisit it only if a
genuinely multi-threaded kernel is ever introduced.

## Where work runs

Never run a simulation, a benchmark, or a full test suite on the login node.

Interactive smoke test:

```bash
srun --account=solverbrict --partition=cpu_amd_dev \
     --ntasks=1 --cpus-per-task=4 --mem=8G --time=00:15:00 --pty bash
```

Batch submission uses `--account=solverbrict --partition=cpu_amd`.

Reference: the full suite passes on a compute node in well under a minute —
`Code/Fracture_fibril` (8 tests) and `Code/Data_analysis` (111 tests).

## Filesystem and I/O

```bash
lfs quota -h "$HOME"
```

- `$HOME` is Lustre and is the only durable storage; the quota is 100 GB. There
  is no separate scratch area — on SDumont2 `$HOME` and `$SCRATCH` are the same
  Lustre filesystem and `/prj` is a symlink into `/scratch`. Watch the quota
  before launching a batch that writes many result files.
- Compute nodes have node-local storage: `/tmp` (492 GB, 455 GB free) and
  `/dev/shm` (756 GB). Both are wiped when the job ends.
- **`SLURM_TMPDIR` is not set on this cluster.** `TMPDIR` is, and points at the
  node-local `/tmp`. Job scripts must fall back through both:
  `${SLURM_TMPDIR:-${TMPDIR:-/tmp}}`, which is what `env.sh` exports as
  `DLA_SCRATCH`.

Simulations are chatty on I/O. Each task should write its scratch files and its
database to `$DLA_SCRATCH` on the node, then copy the finished result to Lustre
and `mv` it into place, so a killed job never publishes a partial file.
`run_array.sbatch` already follows this pattern.

## C++

`g++ 11.4.1` (RHEL 9.4) is available without loading a module, so no compiler
module is needed.

`fast_dla` builds through the makefile, from the repository root:

```bash
make -f Code/Dla/makefile
```

`fast_dla2`, the optimized generator, has no makefile target yet:

```bash
g++ -std=c++17 -O3 -march=native -Wall -Wextra Code/Dla/fast_dla2.cpp -o fast_dla2
```

Build on a compute node, not on the login node. `-march=native` bakes in the
CPU of the machine that compiled it, and the login and compute nodes are not
the same hardware.

## Checking on a batch

```bash
squeue -u "$USER"
sacct -j <JOBID> --format=JobID,State,Elapsed,MaxRSS,ExitCode
```
