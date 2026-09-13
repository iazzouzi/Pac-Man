# Progress Tracking — Planned vs. Actual

The "plan" here is the subject's mandatory checklist (Chapters IV–VI). For each
requirement, the table shows whether it shipped, and the commit(s) that closed it.

| Subject requirement | Status | Landed | Evidence (commit) |
|---|---|---|---|
| JSON config with comments, robust defaults | ✅ Done | Aug 12 | `parser class (preprocess the file from comments and validate the file as a JSON)`, `complete the parser...` |
| Faulty config handling (clamp, no traceback) | ✅ Done | Aug 12–14 | `fix config class`, `config init: level default values fix`, `edit on some range of values to be allowed in the config` |
| Maze generation via external A-Maze-ing package | ✅ Done | Aug 13 | `mazegen a wrapper class inherit from mazegenerator to add custom properties and methods` |
| Persistent highscore system | ✅ Done | Aug 13, Sep 7, Sep 9 | `add highscores_caching mthode` → `Added: top_scores() method` → `Add Ranking sys to HighScoreState` |
| Main menu / game view / game-over UI | ✅ Done | Aug 20–21, Sep 9 | `GameState` architecture, `MainMenuState`, `GameOverState` → merged into `GameResultState` |
| Player movement (4-dir, lives, respawn) | ✅ Done | Aug 16, 21 | player rendering + input, respawn-at-middle-after-death logic |
| Ghosts (chase / flee / respawn) | ✅ Done | Aug 21–22, Sep 9, 11 | BFS-based `identify_target`/`move_ghost`, `edit on the funcionality of the ghosts: let them run away...` |
| Cheat mode | ✅ Done | Aug 25 | `Cheat mode: Invincibility...`, `Cheat mode: Ghost freeze...` |
| Scoring (pacgum / super-pacgum / ghost) | ✅ Done | Aug 14 | pacgum & super-pacgum init, points wired into `Engine` |
| Game progression (≥10 levels, timer, pause/resume) | ✅ Done | Aug 16, Sep 5 | `start_next_level()`, timeout/lives=0 handling, `PauseState` |
| In-game HUD (score, lives, level, time) | ✅ Done | Aug 16, Sep 10 | `draw_score()`, `draw_lives()`, `draw_time()`, HUD extracted to its own class and restyled |
| Instructions screen | ✅ Done | Sep 10 | `Add Instructions state with fixed values` → made config-driven |
| Sound effects | ✅ Done | Sep 9–10 | original Pac-Man SFX added and synced across every state |
| `flake8` / `mypy` compliance | ✅ Done (twice) | Sep 12 | `fixed: Flake&mypy` then `Refix Flake8 after adding Docstrings` |
| Docstrings (PEP 257) | ✅ Done | Sep 12 | `Integrate DocStrings` |
| Makefile (`install/run/debug/clean/lint`) | ✅ Done | Aug 12 | `add Makefile` |
| Packaging (PyInstaller `.spec`, `make package`) | ✅ Done | Sep 12 | `packaging specification script`, `get_asset_path` fix for the frozen build |
| Deployment to a public gaming platform | ✅ Done | Sep 13 | `open_game_page.sh` — https://iazzhim.itch.io/pac-man (`c71cc41`) |
| README with all required sections | ✅ Done | Sep 12 | `README.md` (two commits) |
| Project-management folder | ✅ This folder | Sep 13 | Generated retrospectively from the Git history above |