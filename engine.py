"""Core game engine: level lifecycle, ghost AI, collisions, and scoring."""

import json
import time
from algo import next
from typing import Any, Optional
from models import Config, Player, Ghost
from mazegen import MazeGen
import sys
import os


class Engine:
    """Drives a single game session: levels, entities, and scoring."""

    def __init__(self, config: Config):
        """Initialize engine state from a validated configuration.

        Args:
            config: The game configuration to run with.
        """
        self.highscore_filename = config.highscore_filename
        self.levels = config.levels
        self.lives = config.lives
        self.points_per_pacgum = config.points_per_pacgum
        self.points_per_super_pacgum = config.points_per_super_pacgum
        self.points_per_ghost = config.points_per_ghost
        self.level_max_time = config.level_max_time

        self.player = Player(0, 0, lives=self.lives)

        self.maze: Optional[MazeGen] = None

        self.score = 0

        self.current_level = 0

        self.invincibility = False

        self.ghosts_freeze = False

        self.pacgum_sound: Any = None

        self.fail_sound: Any = None

        self.eating_ghost_sound: Any = None

        self.return_sound: Any = None

        self.edible_ghosts_sound: Any = None

        self.ghosts_move_sound: Any = None

        self.ghosts_move_sound_channel: Any = None

        self.ready_sound: Any = None

        self.ready_sound_channel: Any = None

        self.ready = 0

        self.ready_ts: float = 0

    def initialize_level(self, level: list[int]) -> None:
        """Generate a fresh maze and place the player at its center.

        Args:
            level: A ``[width, height]`` pair describing the level size.

        Raises:
            SystemExit: If the maze generator fails to build the level.
        """
        try:
            self.maze = MazeGen((level[0], level[1]))
        except Exception as e:
            raise SystemExit(e)

        x = level[0] // 2
        y = level[1] // 2

        while self.maze.maze[y][x] == 15:
            x -= 1

        for pacgum in self.maze.pacgums:
            if pacgum.x == x and pacgum.y == y:
                pacgum.available = False
                self.maze.pacgums_nb -= 1

        self.player.x = x
        self.player.y = y
        self.player.base_x = x
        self.player.base_y = y

    def start_next_level(self) -> bool:
        """Advance to and initialize the next level, if any remain.

        Returns:
            ``True`` if a new level was started, ``False`` if all levels
            have already been completed.
        """
        if self.current_level >= len(self.levels):
            return False
        self.initialize_level(self.levels[self.current_level])
        self.current_level += 1
        return True

    def identify_target(self, ghost: Ghost) -> None:
        """Pick a ghost's next target cell and path step toward it.

        Args:
            ghost: The ghost to update.
        """
        assert self.maze is not None
        if ghost.target is not None:
            if ghost.target == (self.player.x, self.player.y):
                if ghost.x == self.player.x and ghost.y == self.player.y:
                    ghost.next = None
                    return
                ghost.next = next(
                    self.maze.maze,
                    (int(ghost.x), int(ghost.y)),
                    ghost.target,
                )
                return

        if ghost.tkal:
            target = (int(ghost.base_x), int(ghost.base_y))

        elif ghost.edible:
            if (
                self.player.x < self.maze._width // 2
                and self.player.y < self.maze._height // 2
            ):
                target = (self.maze._width - 1, self.maze._height - 1)
            elif (
                self.player.x > self.maze._width // 2
                and self.player.y > self.maze._height // 2
            ):
                target = (0, 0)
            elif (
                self.player.x < self.maze._width // 2
                and self.player.y > self.maze._height // 2
            ):
                target = (self.maze._width - 1, 0)
            else:
                target = (0, self.maze._height - 1)

        elif ghost.name == "Blinky":
            target = (self.player.x, self.player.y)

        elif ghost.name == "Pinky":
            if (
                self.player.direction == "up"
                and self.player.y - 2 >= 0
                and self.player.x - 2 >= 0
            ):
                target = (self.player.x - 2, self.player.y - 2)
            elif (
                self.player.direction == "down"
                and self.player.y + 2 <= self.maze._height - 1
            ):
                target = (self.player.x, self.player.y + 2)
            elif self.player.direction == "left" and self.player.x - 2 >= 0:
                target = (self.player.x - 2, self.player.y)
            elif (
                self.player.direction == "right"
                and self.player.x + 2 <= self.maze._width - 1
            ):
                target = (self.player.x + 2, self.player.y)
            else:
                target = (self.player.x, self.player.y)

        elif ghost.name == "Inky":
            for gh in self.maze.ghosts:
                if gh.name == "Blinky":
                    dx = self.player.x - int(gh.x)
                    dy = self.player.y - int(gh.y)
                    if (
                        0 <= self.player.x + dx <= self.maze._width - 1
                        and 0 <= self.player.y + dy <= self.maze._height - 1
                    ):
                        x = self.player.x + dx
                        y = self.player.y + dy
                    else:
                        x = self.player.x
                        y = self.player.y
            target = (x, y)

        elif ghost.name == "Clyde":
            dx = self.player.x - int(ghost.x)
            dy = self.player.y - int(ghost.y)
            if dx * dx + dy * dy > 64:
                target = (self.player.x, self.player.y)
            else:
                target = (int(ghost.base_x), int(ghost.base_y))
        ghost.target = target
        ghost.next = next(
            self.maze.maze, (int(ghost.x), int(ghost.y)), target
        )

    def move_ghost(self, ghost: Ghost) -> None:
        """Step a ghost one increment closer to its next path cell.

        Args:
            ghost: The ghost to move.
        """
        if ghost.next is not None:
            next_x, next_y = ghost.next
            if ghost.tkal:
                speed = 0.2
            else:
                speed = 0.05
            if ghost.x < next_x:
                ghost.direction = "right"
                ghost.x = round(ghost.x + speed, 2)
            elif ghost.x > next_x:
                ghost.direction = "left"
                ghost.x = round(ghost.x - speed, 2)
            if ghost.y < next_y:
                ghost.direction = "down"
                ghost.y = round(ghost.y + speed, 2)
            elif ghost.y > next_y:
                ghost.direction = "up"
                ghost.y = round(ghost.y - speed, 2)

    def update(self) -> Optional[str]:
        """Advance the game state by one tick.

        Returns:
            ``"death"`` if the player was caught by a ghost this tick,
            otherwise ``None``.
        """
        assert self.maze is not None
        if not self.ready:
            if (
                not self.ready_sound_channel
                or not self.ready_sound_channel.get_busy()
            ):
                self.ready_sound_channel = self.ready_sound.play()
                self.ready_ts = time.time()
        if self.ready:
            if (
                not self.ghosts_move_sound_channel
                or not self.ghosts_move_sound_channel.get_busy()
            ):
                self.ghosts_move_sound_channel = (
                    self.ghosts_move_sound.play()
                )
        if not self.ready and time.time() - self.ready_ts > 5.0:
            self.ready = 1
        if not self.ready:
            return None
        for ghost in self.maze.ghosts:
            if ghost.edible:
                if time.time() - ghost.edible_ts > 10.0:
                    self.edible_ghosts_sound.fadeout(1000)
                    ghost.edible = False
            if self.ghosts_freeze:
                continue
            if (
                not ghost.tkal
                and abs(self.player.x - ghost.x) < 0.5
                and abs(self.player.y - ghost.y) < 0.5
            ):
                if ghost.edible:
                    self.eating_ghost_sound.play()
                    self.score += self.points_per_ghost
                    self.return_sound.play()
                    ghost.edible = False
                    ghost.tkal = True
                    ghost.x = round(ghost.x)
                    ghost.y = round(ghost.y)
                elif not self.invincibility:
                    self.ghosts_move_sound.stop()
                    self.edible_ghosts_sound.stop()
                    self.fail_sound.play()
                    self.player.lives -= 1
                    for gh in self.maze.ghosts:
                        gh.edible = False
                        gh.tkal = False
                    self.ready = 0
                    self.ready_sound_channel = None
                    return 'death'
            if ghost.x % 1 == 0 and ghost.y % 1 == 0:
                self.identify_target(ghost)
            self.move_ghost(ghost)
            if ghost.tkal:
                if ghost.x == ghost.base_x and ghost.y == ghost.base_y:
                    self.return_sound.fadeout(1000)
                    ghost.tkal = False

        for pacgum in self.maze.pacgums:
            if (
                pacgum.available
                and self.player.x == pacgum.x
                and self.player.y == pacgum.y
            ):
                self.pacgum_sound.play()
                if pacgum.super:
                    self.score += self.points_per_super_pacgum
                    self.ghosts_move_sound.stop()
                    self.edible_ghosts_sound.play()

                    for ghost in self.maze.ghosts:
                        if ghost.tkal:
                            continue
                        ghost.edible = True
                        ghost.edible_ts = time.time()
                else:
                    self.score += self.points_per_pacgum

                pacgum.available = False
                self.maze.pacgums_nb -= 1
        return None

    def reset_after_death(self) -> None:
        """Return the player and all active ghosts to their spawn points."""
        assert self.maze is not None
        self.player.x = self.player.base_x
        self.player.y = self.player.base_y
        for gh in self.maze.ghosts:
            if gh.tkal:
                continue
            gh.x = gh.base_x
            gh.y = gh.base_y

    @staticmethod
    def highscores_caching(
        name: str, score: int, highscore_filename: str
    ) -> None:
        """Append a new highscore entry and persist the sorted list.

        Args:
            name: The player's name.
            score: The player's final score.
            highscore_filename: Path to the JSON highscore file.
        """
        data: list[dict[str, Any]] = []
        try:
            with open(highscore_filename, "r") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError, Exception):
            pass
        try:
            with open(highscore_filename, "w") as file:
                data.append({"name": name, "score": score})
                json.dump(
                    sorted(
                        data, key=lambda x: (x["score"], x["name"]),
                        reverse=True,
                    ),
                    file,
                )
        except (OSError, Exception) as e:
            print(f"Error occurred while writing to highscore file: {e}")

    def get_top_scores(self) -> dict[str, int]:
        """Load the highscore file and return the top 10 entries.

        Returns:
            A mapping of player name to score, limited to 10 entries.
        """
        loaded = {}
        file = self.highscore_filename
        try:
            with open(file, 'r') as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError, Exception):
            return {}
        for dict_ in data:
            loaded[dict_['name']] = dict_['score']
        return {key: loaded[key] for key in list(loaded)[:10]}

    @staticmethod
    def get_asset_path(relative_path: str) -> str:
        """Get the absolute path to an asset, compatible with PyInstaller.

        Args:
            relative_path: The relative path to the asset file.

        Returns:
            The absolute path to the asset file.
        """
        try:
            base_path = sys._MEIPASS  # type: ignore
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
