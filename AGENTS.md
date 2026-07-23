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

## Agent skills

### Issue tracker

Issues and revision Specs are tracked in GitHub Issues for `michaelsouza/dla-collagen`; external pull requests are not a triage request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the canonical labels `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repository. Read the root domain context and relevant ADRs when they exist. See `docs/agents/domain.md`.
