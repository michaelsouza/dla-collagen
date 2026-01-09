# Repository Guidelines

## Project Structure

- `paper_collagen.tex`: main manuscript (Biophysical Journal LaTeX).
- `sample.bib`: BibTeX database.
- `biophys-new.cls`, `biophysj.bst`: journal class and bibliography style.
- `figure_*.pdf`: figures used by the LaTeX build.
- `figure_*.png`: figure previews (not used by the build).
- `prompts/`: prompt templates for review/edit workflows.
- `review-*.md`: generated review notes.

## Build, Test, and Development Commands

Prerequisites: a LaTeX distribution that provides `pdflatex` and `bibtex`.

- `make`: builds `paper_collagen.pdf` (LaTeX → BibTeX → LaTeX ×2).
- `make clean`: removes auxiliary files and the generated PDF.

Tip: after changing citations or the `.bib`, run `make clean && make` to avoid stale `.bbl` output.

## Writing Style & Naming Conventions

- Keep scientific meaning unchanged unless the change is explicitly requested.
- Maintain consistent notation (e.g., choose `$T_s$` vs `$T_{s}$` and use it everywhere).
- Use nonbreaking spaces before refs/cites (`Figure~\ref{...}`, `et al.~\cite{...}`) to prevent bad line breaks.
- Keep figure filenames stable (`figure_1.pdf`, …). If replacing a figure, update the matching `.pdf` (build) and `.png` (preview).

## Testing Guidelines

There are no automated tests. Treat a clean LaTeX build as the primary validation: no missing references/citations and no errors.

## Commit & Pull Request Guidelines

- Git history is currently minimal (single initial commit). Use clear, imperative subjects (e.g., `paper: fix grammar in abstract`, `fig: update Figure 2`).
- PRs should describe what changed (tex/bib/figures), include the rendered PDF (or page screenshots) for affected sections, and list any new build prerequisites.

## Security & Generated Files

Do not commit secrets. Build artifacts are ignored via `.gitignore`; prefer committing sources (`.tex`, `.bib`, figures) rather than locally generated outputs.
