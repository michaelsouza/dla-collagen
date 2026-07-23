# Handoff: ER12738 manuscript revision

This handoff lets the revision continue on another computer without reconstructing the decisions from chat history.

## Start here

1. Check out the branch `codex/revision-handoff-issue-9`.
2. Read `AGENTS.md`.
3. Read the umbrella [Revision Spec #1](https://github.com/michaelsouza/dla-collagen/issues/1) and its native sub-issues/dependencies.
4. Read the original referee reports in `Reviews/Referees-comment-Suki.md`.
5. Inspect the current manuscript diff before continuing Issue #9.

## Tracker state

- The major revision is coordinated by [Spec #1](https://github.com/michaelsouza/dla-collagen/issues/1).
- Eleven implementation tickets exist as sub-issues, #2 through #12, with native GitHub blocking relationships.
- The initial unblocked frontier is #2 (data/reproducibility audit), #3 (rupture protocol), #9 (physical interpretation of the surface-relaxation parameter), and #10 (coarse-graining and phenomenological fit).
- The critical chain is rupture protocol → avalanche definition → statistical reanalysis → interpretation → manuscript revision → response letter.

## Issue #9 status

[Issue #9](https://github.com/michaelsouza/dla-collagen/issues/9) is in progress and remains open.

The current manuscript and bibliography changes:

- define the surface-relaxation parameter as a dimensionless kinetic control parameter;
- introduce the conceptual relaxation/growth balance through the ratio of deposition and relaxation timescales;
- discuss the qualitative influence of temperature, collagen concentration, pH, ionic strength, and buffer composition;
- explicitly reject a one-to-one quantitative mapping to a single experimental variable;
- add seven supporting bibliography entries.

The evidence, build result, acceptance status, and partial response to R1-1 are recorded in the [Issue #9 evidence comment](https://github.com/michaelsouza/dla-collagen/issues/9#issuecomment-5060402096).

Issue #9 must not be closed yet. Its remaining work is:

- distinguish omitted cellular positioning from the modeled random surface walk;
- state what experimental data and calibration would be required to map the parameter quantitatively;
- reconcile the interpretation across Methods, Discussion, and Conclusion;
- remove or sharply qualify unsupported evolutionary and disease extrapolations;
- finalize the point-by-point response to R1-1 with manuscript locations.

## Repository state captured by this branch

The branch includes three local commits that previously had not reached `origin/main`:

- the Clauset et al. power-law reference in PDF and Markdown form;
- the Yang and Kaufman reference PDF;
- removal of generated LaTeX artifacts from version control and corresponding ignore rules.

It also includes:

- the current Issue #9 manuscript and bibliography changes;
- repository-wide revision instructions in `AGENTS.md`;
- issue-tracker, triage-label, and domain-document conventions under `docs/agents/`;
- this handoff.

The apparent local modification to `Code/Fracture_fibril/run_parallel.sh` was only a Windows Git file-mode artifact. The executable bit is unchanged in the WSL checkout and the file is not part of the intended commit.

## Validation already performed

- The manuscript was compiled with `latexmk` in an isolated output directory.
- Build exit code: 0.
- BibTeX resolved the seven new references.
- No undefined citations or references were reported.
- Remaining warnings were the existing `nameref` label-definition warning and two float-placement adjustments.

## Suggested next actions

1. Continue the remaining acceptance criteria in Issue #9.
2. Recompile the manuscript in an isolated output directory.
3. Add the final evidence and manuscript locations to Issue #9.
4. Close Issue #9 only when every acceptance criterion is satisfied.
5. Then select another unblocked frontier ticket from Spec #1.

## Suggested skills

- `github:github` for reading and updating the Spec and ticket evidence.
- `mattpocock-skills:implement` for executing one ready revision ticket.
- `mattpocock-skills:research` when additional primary-source support must be captured in the repository.
- `mattpocock-skills:handoff-local` before moving the work between environments again.
- `github:yeet` when publishing the next completed set of local changes.
