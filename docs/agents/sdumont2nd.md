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

### The submit limit is the binding constraint

QOS `ict_cpu-genoa` sets `MaxSubmitJobsPU=100` and leaves `MaxJobsPU`
unlimited. **Every element of a job array counts as one submitted job**, so the
cap is 100 array tasks in the queue at any moment, summed over all of your
jobs. `%N` throttling does not help: it limits how many tasks run
concurrently, not how many are submitted.

Verify before designing a batch, and note that `sacctmgr -nP` emits an extra
empty column that makes `MaxJobsPU` easy to misread as the submit limit — ask
for the header:

```bash
sacctmgr -P show qos ict_cpu-genoa format=Name,MaxWall,MaxTRESPU,MaxJobsPU,MaxSubmitJobsPU
sbatch --test-only --account=solverbrict --partition=cpu_amd --array=0-99 script.sbatch
```

`--test-only` validates against the live QOS without submitting, and is the
cheapest way to confirm a batch will be accepted. A campaign larger than 100
tasks has to be split into successive arrays — chained with `--dependency`, or
re-submitted as tasks drain.

Other limits: `MaxTRESPU` is 1920 CPUs and 14976 GB per user, there is no
wall-clock cap on `cpu_amd`, and `MaxArraySize` is 1001 (never the binding
constraint here, given the submit cap).

`Code/Fracture_fibril/slurm/run_array.sbatch` predates this cluster: its
`--array=0-299%150` is rejected outright.

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
`DLA_PARTITION`, `DLA_PARTITION_DEV`, `DLA_REPO`, and `DLA_TMP`. It is
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

Two Lustre areas matter, with very different sizes. Check both before
launching a batch:

```bash
lfs quota -h -p "$(id -u)" /petrobr        # personal home quota
lfs quota -h -g solverbrict /petrobr       # project area (~/scratch)
```

**Home** (`$HOME` = `/petrobr/parceirosbr/home/<user>`) has a **100 GB**
project quota. It holds the clone, the venv, and nothing else. It is not
sized for simulation output.

**Project area** (`/petrobr/parceirosbr/solverbrict`) has a **6 TB** group
quota, shared with the other `solverbrict` users and roughly 2.6 TB full as of
August 2026. It is group-writable and setgid, so files created there inherit
the `solverbrict` group. This is where production results belong.

`~/scratch` is a symlink to the personal directory inside that area, and
`env.sh` exports its resolved path as `$DLA_PROJECT`
(`.../solverbrict/<user>/dla-collagen`). Two consequences worth keeping in
mind: anything written through `~/scratch` counts against the **group** quota,
not the home quota, so `lfs quota -g solverbrict /petrobr` is the number to
watch; and any tool that copies `$HOME` while following symlinks would try to
pull the whole project area with it.

The quota is shared with other people. Check it before a large batch and clean
up afterwards.

Two things that look like extra space but are not: `$SCRATCH` is merely an
alias for `$HOME`, and the 3 PB `/scratch` filesystem (with `/prj`, a symlink
into it) belongs to other projects and denies us write access.

Compute nodes have node-local storage: `/tmp` (492 GB, 455 GB free) and
`/dev/shm` (756 GB). Both are wiped when the job ends.

**`SLURM_TMPDIR` is not set on this cluster.** `TMPDIR` is, and points at the
node-local `/tmp`. Job scripts must fall back through both:
`${SLURM_TMPDIR:-${TMPDIR:-/tmp}}`, which is what `env.sh` exports as
`DLA_TMP`.

Simulations are chatty on I/O. Each task should write its scratch files and its
database to `$DLA_TMP` on the node, then copy the finished result to the
project area and `mv` it into place, so a killed job never publishes a partial
file. `run_array.sbatch` already follows this pattern.

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
