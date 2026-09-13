# Project Analysis & Technical Choices

## Architecture split

The codebase cleanly separates **logic** from **presentation**, which is also
how the two authors split their work (see `05-team-organization.md`):

- `parser.py`, `models.py`, `engine.py`, `algo.py`, `mazegen.py`, `pac-man.py`
  — headless game logic, no Pygame drawing calls.
- `gui.py` + `gui_src/*` — a `GameState` state-machine (menu, playing, pause,
  result, highscore, instructions) that only ever talks to the engine, never
  the other way around.

This choice paid off during the project: the engine and the GUI could be built
and iterated on largely in parallel (Ibrahim on `engine.py`/`algo.py`, Adam on
`gui_src/`) with only a handful of merge points, and just one recorded merge
conflict in five weeks (`3338de6 conflict`, Aug 21).

## Config parsing with comment support

The subject requires a "JSON with comments" config format. Rather than hand-roll
a full tokenizer, `Parser.filePreprocess` strips `#`/`//` comment lines before
handing the result to the standard `json` module — the pragmatic option given
the time budget, at the cost of not tolerating trailing/inline comments on the
same line as a value (acceptable given the subject only asks for "lines
starting with #").

## Pathfinding: BFS over a full ghost-AI model

The subject leaves ghost behavior open ("distance-based, random, etc."). The
team implemented a shared BFS shortest-path module (`algo.py`) reused by every
ghost, with each ghost differentiated only by its **target cell** —
`identify_target()` decides that target per ghost (e.g. Blinky targets Pac-Man
directly). This gave four distinct ghost personalities from one pathfinding
implementation instead of four separate algorithms, at the cost of extra
iteration to get "flee when edible" and "respawn to corner" behaving correctly
(three follow-up commits between Aug 21–22 and again Sep 11).

## Maze generator integration

Per the subject's constraint ("you must not write your own generator"),
`mazegen.py` wraps the assigned `A-Maze-ing` package (shipped in-repo as
`mazegenerator-00001-py3-none-any.whl`) instead of modifying it. `MazeGen`
inherits from `MazeGenerator` purely to layer Pac-Man's own entity placement
(pacgums, super-pacgums in the 4 corners, ghost spawn points) on top of the
generator's raw corridor output, matching the subject's requirement that "your
loader must adapt to their interface, not the opposite."

## GUI state machine

The GUI went through one real redesign: an early flat set of screens (Aug 16)
was replaced (Aug 20) by a proper `GameState` base class using inheritance and
method overriding, then later consolidated further (Sep 9) by merging separate
victory/game-over screens into one `GameResultState`. Each rewrite reduced
duplicated event/render code rather than adding new screens — a sign the team
was refactoring for maintainability under a deadline rather than just bolting
on features.

## Packaging

`make package` builds a PyInstaller one-file executable from `pac-man.spec`,
bundling `assets/`, `resources/`, `config.json`, and `instructions.txt`. This
surfaced a real bug specific to frozen builds: paths that work when run with
`python3 pac-man.py` break inside PyInstaller's temp extraction folder. It was
fixed with a dedicated `get_asset_path()` helper adopted at every asset-loading
call site (`7a373e5`, `593d756`) — a good example of a problem that only shows
up once you actually package the thing, not while running it from source.
