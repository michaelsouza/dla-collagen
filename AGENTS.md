# Repository guidance

These instructions apply to the entire repository.

## Manuscript revision workflow

The current priority is the major revision of manuscript ER12738, *Scaling behaviors in simulated collagen fibrils*.

- Use [GitHub issue #1](https://github.com/michaelsouza/dla-collagen/issues/1) as the umbrella revision Spec.
- Track the revision through one umbrella GitHub Spec issue and a set of linked implementation issues.
- Use issues as the coordination and decision trail. Keep the consolidated scientific record with the manuscript under `Reviews/`, including the revision spec and the response to the referees.
- Preserve traceability to the reports: every ticket must name all referee comments it addresses, even when one ticket resolves comments from both referees.
- Organize tickets around a scientific decision or independently verifiable deliverable, not mechanically one ticket per numbered referee comment.
- Treat a blocking edge as a real gate: use it only when the blocker can change or invalidate the downstream work. Record native GitHub issue dependencies and repeat them in the ticket body for portability.
- Follow the critical chain: rupture protocol → avalanche definition → statistical reanalysis → interpretation of the avalanche exponent and load sharing → manuscript revision → response letter.
- Work only on tickets whose blockers are closed. Before editing a claim, read the umbrella Spec, the relevant ticket, and its dependency history.
- Each ticket must contain: parent Spec, referee comments addressed, scientific question or decision, end-to-end deliverable, acceptance criteria, blockers, evidence/results, final decision, and proposed response to the referees.
- Do not use Self-Organized Criticality, scale-free behavior, or local/global load-sharing universality as established conclusions unless a completed ticket supplies explicit statistical and mechanistic support.
- Distinguish empirical correlations from causal or theoretical relationships, especially for the relation between cross-sectional fractal dimension and rupture statistics.
- Preserve unrelated local changes. Do not rewrite or discard existing manuscript, bibliography, data, or simulation edits while working on a revision ticket.

## Cluster runs (SDumont2)

Production runs execute on SDumont2 (LNCC), account `solverbrict`, partition `cpu_amd` (`cpu_amd_dev` for tests). See `docs/agents/sdumont2nd.md`.

- Move code between the laptop and the cluster through git only; never copy a working tree.
- Activate the environment with `source Code/cluster/sdumont2nd/env.sh` at the start of every session and at the top of every job script. Do not build a new conda environment: the `anaconda3/2024.10` module already covers `requirements.txt`.
- Never run a simulation, benchmark, or full test suite on the login node.
- Write per-task scratch and databases to node-local storage (`$DLA_TMP`), then copy the finished file to Lustre and `mv` it into place, so an interrupted job never publishes a partial result.
- Write production results to `$DLA_PROJECT` (`~/scratch/dla-collagen`, in the 6 TB `solverbrict` project area), never to `$HOME`, whose 100 GB quota fits only the clone and the venv. The project quota is shared with other users; check it before a large batch. `$SCRATCH` is an alias for `$HOME` and buys no extra space.
- `SLURM_TMPDIR` does not exist on SDumont2; fall back through `${SLURM_TMPDIR:-${TMPDIR:-/tmp}}`.
- Respect the QOS caps: 100 running jobs and 300 submitted jobs per user. Throttle job arrays to at most `%100`.
- Record in the relevant ticket which cluster, partition, and job ID produced any result that enters the manuscript.

## Agent skills

### Issue tracker

Issues and revision Specs are tracked in GitHub Issues for `michaelsouza/dla-collagen`; external pull requests are not a triage request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the canonical labels `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repository. Read the root domain context and relevant ADRs when they exist. See `docs/agents/domain.md`.
