# Blocking Points & Conflicts

## 1. Nine-day inactivity gap (Aug 26 – Sep 4)

The single biggest blocking period in the project: zero commits from either
author for 9 straight days, between the "playable loop" phase (cheat modes
landed Aug 25) and the "feature completion sprint" (PauseState, Sep 5). This
pushed a meaningful share of the remaining mandatory work — pause/resume,
highscores UI, instructions screen, all sound effects, all polish, all
linting/typing/docstrings, and packaging — into the final ~7 days, with over
half of all commits (57/123) landing in the final week and a third of all
commits landing on submission day itself (Sep 12).

**Effect:** no evidence of harm to the final deliverable, but it's the reason
lint/type-checking ended up being a same-day, twice-repeated task instead of a
continuous one (see below), and the reason packaging/asset-path bugs were
caught on submission day rather than earlier.

## 2. One explicit merge conflict (Aug 21)

Commit `3338de6` is simply titled `conflict`, right in the middle of the
ghost-behavior and respawn-logic work (both authors were editing overlapping
areas of `engine.py`/`gui.py` that day). It was resolved same-day; no further
conflicts are recorded in the other 122 commits, consistent with the
logic/GUI split holding up for the rest of the project.

## 3. Lint/type-checking had to be redone the same day

`fixed: Flake&mypy` (12:46, Sep 12) was followed a few hours later by
`Refix Flake8 after adding Docstrings` (15:14, Sep 12) — adding the required
PEP 257 docstrings reintroduced `flake8` violations that had just been fixed.
This is a process point more than a bug: running `make lint` only right before
submission means every later change (docstrings included) can silently break
it again.

## 4. The ghost "stop" bug was fixed twice

`update identify_target function` (Sep 11, 18:28) addressed ghosts getting
stuck, but the same class of bug reappeared and needed a second, final fix
(`fix the ghosts stop problem`, Sep 12, 20:49) — the very last commit before
submission. This indicates the first fix addressed a symptom rather than the
root cause of the pathfinding target logic, and it's worth re-testing
specifically for edge cases (e.g. ghosts in corners or dead-ends) during the
peer review's recode step, since it was fixed under time pressure and wasn't
re-verified over a longer play session.

## 5. Platform deployment landed a day after the rest of the project

The subject requires deployment to a public gaming platform (Steam/itch.io) as
an unlisted/private build. This was the one mandatory item not closed out on
submission day: it landed Sep 13, one day after everything else, with
`open_game_page.sh` pointing to the unlisted itch.io page
(https://iazzhim.itch.io/pac-man). Not a real blocker in the end, but a sign
that platform packaging/upload is worth scheduling alongside the PyInstaller
work on the main submission day rather than after it, in case the platform's
review or upload step takes longer than expected.
