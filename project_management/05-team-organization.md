# Team Organization

Team of two: **iazzouzi (Ibrahim)** and **Adam Khalil** (committing under two
GitHub handles, `4d4mKhalil` and `adkhalil`, same email address).

## Commit share

| Author | Commits | Lines added | Lines removed |
|---|---|---|---|
| Ibrahim (`iazzouzi`) | 78 | 1,719 | 659 |
| Adam Khalil (`4d4mKhalil` + `adkhalil`) | 45 | 3,271 | 1,060 |
| **Total** | **123** | **4,990** | **1,719** |

Ibrahim made more, smaller commits (mostly logic and bug fixes); Adam made
fewer, larger commits (mostly GUI screens and assets), which is why the lines-
changed ranking is the reverse of the commit-count ranking.

## Who owned what (by files actually touched)

**Ibrahim — core engine & logic**
- `parser.py` — config parsing/validation (12 commits)
- `engine.py` — game loop, level lifecycle, scoring, cheat mode (39 commits)
- `models.py` — `Player`, `Pacgum`, `Ghost`, `Config` data classes (10 commits)
- `algo.py` — BFS pathfinding for ghost movement (4 commits)
- `mazegen.py` — wrapper around the assigned `A-Maze-ing` package (16 commits)
- `pac-man.py` — entry point (4 commits)
- Sound effects wiring across game states
- Packaging: `pac-man.spec`, `make package`, the `get_asset_path()` fix

**Adam Khalil — GUI & presentation**
- `gui.py` / `gui_src/__init__.py` — Pygame init, state machine plumbing
- `gui_src/menu_state.py`, `game_state.py` — main menu, base `GameState`
- `gui_src/playing_state.py` — HUD, rendering, animations (13 commits, the
  single most-touched GUI file)
- `gui_src/pause_state.py`, `result_state.py` — pause menu, game-over/victory
- `gui_src/highscore_state.py` — highscore ranking/medal UI
- `gui_src/instructions_state.py`, `background.py` — instructions screen,
  animated background
- `top_scores()` highscore ranking method

**Shared / overlapping**
- `gui.py` and `pac-man.py` were touched by both (14 vs 13, and 4 vs 2,
  commits respectively) — expected for the two files that glue engine and GUI
  together.
- Final-day lint/type/docstring cleanup (`fixed: Flake&mypy`, `Refix Flake8
  after adding Docstrings`, `Integrate DocStrings`) was split across both
  authors rather than owned by one person.

## How decisions were made

The repository shows an informal, direct-to-`main` workflow rather than a
feature-branch/PR process — there's no branch history beyond `main`, and only
3 explicit merge commits (all local `main`↔`origin/main` syncs on Sep 10).
Task division followed the logic/GUI split described above organically rather
than through a formal sign-off process; commit messages (including some
written casually in Darija — e.g. `walo`, `awel wa7ed yl3eb`) suggest a
low-ceremony, fast-iteration working style typical of a small, trusted team
under a deadline.

## How issues were handled

Bugs were fixed close to when they were introduced rather than batched: e.g.
the pacgum-count bug (Aug 13) was fixed within the same day, and the ghost
"stop" bug was found and fixed twice, a day apart (Sep 11 and again Sep 12),
showing the first fix was incomplete and had to be revisited. See
`06-acceptance-tests.md` for the full bug list and `07-blocking-points.md` for
where things visibly stalled or had to be redone.
