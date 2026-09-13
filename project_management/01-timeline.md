# Project Timeline

Derived from `git log --all --date=iso` on the `main` branch (123 commits total,
78 by **iazzouzi**, 45 by **Adam Khalil** — committing as `4d4mKhalil` and
`adkhalil`, same author, same email).

Total elapsed calendar time: **Aug 11, 2026 → Sep 12, 2026** (33 days), with an
inactive stretch of 9 days in the middle (see "Gap" below).

## Gantt view

```mermaid
gantt
    title Pacman — actual delivery timeline
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b

    section Foundations (Ibrahim solo)
    Config parser + Config class            :done, f1, 2026-08-11, 2026-08-12
    Engine skeleton + game loop draft        :done, f2, 2026-08-13, 2026-08-14
    Models (Player, Pacgum, Ghost)           :done, f3, 2026-08-13, 2026-08-14
    A-Maze-ing wrapper (mazegen.py)          :done, f4, 2026-08-13, 2026-08-13
    Highscore caching (first draft)          :done, f5, 2026-08-13, 2026-08-13

    section Rendering bootstrap (Adam joins)
    Pygame window + maze/cell rendering      :done, r1, 2026-08-15, 2026-08-16
    BFS pathfinding module (algo.py)         :done, r2, 2026-08-15, 2026-08-16
    Player movement + HUD (score/time)       :done, r3, 2026-08-16, 2026-08-16

    section Playable loop
    GameState architecture (inheritance)     :done, g1, 2026-08-20, 2026-08-20
    MainMenuState / GameOverState            :done, g2, 2026-08-20, 2026-08-21
    Ghost AI (chase/flee) + respawn logic    :done, g3, 2026-08-21, 2026-08-22
    Cheat mode: invincibility + ghost freeze :done, g4, 2026-08-24, 2026-08-25

    section Inactive period
    No commits (break)                       :crit, gap, 2026-08-26, 2026-09-04

    section Feature completion sprint
    PauseState + top_scores()                :done, s1, 2026-09-05, 2026-09-07
    Ghost animations + Inky targeting         :done, s2, 2026-09-08, 2026-09-09
    Sound effects across all states           :done, s3, 2026-09-08, 2026-09-09
    HighscoreState + InstructionsState        :done, s4, 2026-09-09, 2026-09-10

    section Polish & UX
    FPS fix, animated background, HUD restyle:done, p1, 2026-09-10, 2026-09-10
    Ranking/medal UI, arcade font & colors    :done, p2, 2026-09-10, 2026-09-11

    section Hardening & delivery
    flake8 / mypy cleanup + docstrings        :done, h1, 2026-09-12, 2026-09-12
    PyInstaller packaging + asset path fix    :done, h2, 2026-09-12, 2026-09-12
    README + final ghost-stop bug fix         :crit, h3, 2026-09-12, 2026-09-12
```

## Phase-by-phase narrative

1. **Foundations — Aug 11–14 (Ibrahim solo).** Config parsing with comment
   stripping and validation, the `Engine` game-loop skeleton, the core
   `Player`/`Pacgum`/`Ghost` models, the `A-Maze-ing` wrapper class, and a first
   pass at highscore caching. No GUI yet.
2. **Rendering bootstrap — Aug 15–16 (Adam joins).** First Pygame window, maze
   and wall rendering from the bitwise maze representation, centered
   pacgum/maze drawing, keyboard input, score/time HUD. In parallel Ibrahim
   built the BFS pathfinding module and fixed early pacgum-count bugs.
3. **Playable loop — Aug 20–25.** The GUI was rewritten around a `GameState`
   state-machine (inheritance/polymorphism) with `MainMenuState` and
   `GameOverState`. Ghosts became "alive" (chase the player, flee when edible,
   respawn at their base), and both cheat-mode features required by the
   subject (invincibility, ghost freeze) were added.
4. **Inactive period — Aug 26–Sep 4 (9 days).** No commits from either author.
5. **Feature completion sprint — Sep 5–9.** `PauseState`, the highscore
   `top_scores()` ranking method, ghost animations, the Inky targeting
   algorithm, and sound effects synced across every state.
6. **Polish & UX — Sep 10–11.** FPS fixed at 30, animated scrolling
   background, HUD restyle, medal-based highscore UI, arcade-style font and
   colors.
7. **Hardening & delivery — Sep 12 (submission day).** `flake8`/`mypy`
   cleanup (done twice — see `07-blocking-points.md`), docstrings added
   project-wide, the PyInstaller `.spec` and `make package` rule, the asset-path
   fix needed for the packaged build, the README, and the final ghost-behavior
   bug fix at 20:49, the last commit before submission.
