# Project Management — Pacman (42 / A-Maze-ing subject)

This folder contains the project-management evidence required by **Chapter VIII** of
the subject. Unlike a plan written before the fact, most of it is a **retrospective
analysis built directly from the Git history** of the repository
(https://github.com/iazzouzi/Pac-Man), since the team ran the project as two
people committing straight to `main` rather than through formal tickets. Where a
GitHub Projects / Kanban board was used, a link or screenshot should be dropped
into `05-team-organization.md` (the raw GitHub API was rate-limited while these
documents were generated, so board contents couldn't be pulled automatically).

## Contents

| File | What it covers |
|---|---|
| [`01-timeline.md`](01-timeline.md) | Actual project timeline (Gantt-style), phase by phase, built from commit dates |
| [`02-progress-tracking.md`](02-progress-tracking.md) | Planned scope (from the subject) vs. what actually shipped, and when |
| [`03-project-analysis.md`](03-project-analysis.md) | Key technical choices and why they were made |
| [`04-risk-analysis.md`](04-risk-analysis.md) | Risks identified during the project and how they were mitigated |
| [`05-team-organization.md`](05-team-organization.md) | Who did what, how decisions were made, how issues were handled |
| [`06-acceptance-tests.md`](06-acceptance-tests.md) | Features tested, bugs found and fixed |
| [`07-blocking-points.md`](07-blocking-points.md) | Blocking points and conflicts during the project |

## Source of data

All numbers, dates, authorship and file-ownership figures in these documents come
from `git log`, `git shortlog`, and `git log --numstat` run against the `main`
branch of the repository (123 commits, Aug 11 2026 – Sep 12 2026). Nothing here is
invented — where information could not be verified from the repo alone (e.g. the
itch.io/Steam listing, or any GitHub Projects board), it is flagged explicitly
instead of guessed.
