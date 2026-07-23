# Issue tracker: GitHub

Issues, revision Specs, and implementation tickets for this repository live in GitHub Issues at `michaelsouza/dla-collagen`.

The active ER12738 manuscript revision is coordinated by [issue #1](https://github.com/michaelsouza/dla-collagen/issues/1).

## Conventions

- Infer the repository from the `origin` remote.
- Publish a Spec as one umbrella issue.
- Publish each approved ticket as a separate issue and link it to the umbrella issue as a sub-issue when GitHub supports the relationship.
- Use GitHub's native issue dependencies for blocking edges. Also list the blockers in the ticket body so the dependency remains visible outside the GitHub UI.
- Apply `ready-for-agent` only when an issue is fully specified and can be completed without additional unstated context.
- Do not close or rewrite the parent Spec while publishing its tickets.
- External pull requests are not a triage request surface for this repository.

## When a skill says "publish to the issue tracker"

Create a GitHub issue in `michaelsouza/dla-collagen`.

## When a skill says "fetch the relevant ticket"

Read the full issue body, comments, labels, parent Spec, sub-issues, and blocking relationships before starting work.

## Revision frontier

The active frontier consists of open revision tickets that have no open blockers and no active assignee. Work one frontier ticket at a time and attach the resulting evidence, commit, or pull request to that issue.
