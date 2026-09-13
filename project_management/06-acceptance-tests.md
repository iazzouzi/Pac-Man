# Acceptance Test Plan

The subject explicitly asks for "features tested, bugs found/fixed" as
project-management evidence (test code itself is not graded per Chapter III.3).
This is a manual acceptance checklist derived from the mandatory feature list
in Chapters IV–VI, plus the actual bug history pulled from commit messages.

## Manual acceptance checklist

| Feature | How to verify | Status |
|---|---|---|
| Program launches with `python3 pac-man.py config.json` | Run from a clean checkout | ✅ |
| Missing/invalid config file handled without a traceback | Run with a nonexistent path, and with a config missing keys / out-of-range values | ✅ (clamped to defaults per `parser.py`) |
| Comments (`#`) stripped from config before parsing | Add a `#` line to `config.json` and reload | ✅ |
| Maze generated via `A-Maze-ing`, `PERFECT=False` corridors | Start a game, inspect corridor shapes | ✅ |
| First level uses a fixed seed, later levels random | Restart the game twice, compare level 1 layouts vs. later levels | ✅ |
| Player moves in 4 directions, blocked by walls | Try walking into a wall | ✅ |
| Player loses a life on ghost contact, respawns at center | Let a ghost catch the player | ✅ |
| Game over at 0 lives; victory at last level cleared | Play to either end state | ✅ |
| Pacgum / super-pacgum / edible-ghost scoring | Eat each and check the HUD score | ✅ |
| Ghosts chase when not edible, flee when edible, respawn after being eaten | Eat a super-pacgum, chase a ghost, let it respawn | ✅ |
| Cheat mode: invincibility | Toggle in-game, confirm ghost contact doesn't cost a life | ✅ |
| Cheat mode: ghost freeze | Toggle in-game, confirm ghosts stop moving | ✅ |
| Pause/resume | Pause mid-level, resume, confirm state is preserved | ✅ |
| Highscore persists across runs, top 10, shown in main menu | Finish a game, enter a name, restart the app | ✅ |
| Highscore name validation (max 10 chars, alphanumeric + spaces) | Try entering a too-long or symbol-heavy name | ✅ (per README's documented behavior) |
| Instructions screen reflects actual config values | Open Instructions, compare against `config.json` | ✅ |
| Sound effects play and stay in sync across menu/pause/playing/game-over | Play through a full session with sound on | ✅ (multiple sync fixes landed Sep 9–10) |
| `make install / run / debug / clean / lint` all work | Run each target | ✅ |
| `flake8` and `mypy` (non-strict flags from the subject) pass | `make lint` | ✅ (as of the final Sep 12 commits) |
| `make package` produces a working standalone build | Run `make package`, launch the produced binary, confirm assets load | ✅ (after the `get_asset_path()` fix) |
| Game is installable from a public platform (Steam/itch.io) | Open https://iazzhim.itch.io/pac-man and install from there | ✅ (unlisted itch.io page, `open_game_page.sh` added Sep 13) |

## Bugs found and fixed (from commit history)

| Date | Bug | Fix |
|---|---|---|
| Aug 12 | Config class produced incorrect values | `fix config class` |
| Aug 13 | Incorrect pacgum count on init | `pacgums number bug` |
| Aug 14 | Level defaults not applied correctly | `config init: level default values fix` |
| Aug 16 | Pacgums initialized on wrong cells | `fix pacgums initializing bug` |
| Aug 16 | BFS `next()` logic produced wrong moves | `fix algo next logic bugs` |
| Aug 16 | Maze/HUD centering offset wrong | `Fix offset_x/y Calculation for Centering` |
| Aug 21 | `IndexError: list index out of range` in `next()` | `fix list index out of range in the next function` |
| Sep 9 | Sound effects didn't play correctly in pause / victory / game-over states | Two dedicated fix commits |
| Sep 10 | Frame rate unstable, movement speed felt wrong | `Fixed Fps problem and let the player moves by 2cell/sec instead of 10` |
| Sep 10 | Sound bug (regression from prior sync fixes) | `fix a sound bug` |
| Sep 11 | Ghosts could get stuck ("stop problem") | `update identify_target function` |
| Sep 12 | Ghost-stop bug resurfaced | Second, final fix — `fix the ghosts stop problem` (last commit before submission) |
| Sep 12 | `flake8`/`mypy` violations | `fixed: Flake&mypy` |
| Sep 12 | New `flake8` violations introduced by docstrings | `Refix Flake8 after adding Docstrings` |
| Sep 12 | Player movement animation broken | `fix player movement animation` |
| Sep 12 | Assets fail to load from a PyInstaller-frozen build | `get_asset_path()` adopted everywhere assets are loaded |
