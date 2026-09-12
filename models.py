"""Data classes representing the core game entities.

Defines the plain-data containers used throughout the game: the parsed
configuration, the player, pacgums, and ghosts.
"""

from typing import Optional


class Config:
    """Holds all tunable game parameters loaded from the config file."""

    def __init__(
        self,
        highscore_filename: str,
        levels: list[list[int]],
        lives: int,
        points_per_pacgum: int,
        points_per_super_pacgum: int,
        points_per_ghost: int,
        level_max_time: float,
    ):
        """Initialize the configuration values.

        Args:
            highscore_filename: Path to the JSON file used to persist
                highscores.
            levels: List of ``[width, height]`` pairs, one per level.
            lives: Number of lives the player starts with.
            points_per_pacgum: Score awarded for eating a pacgum.
            points_per_super_pacgum: Score awarded for eating a
                super-pacgum.
            points_per_ghost: Score awarded for eating an edible ghost.
            level_max_time: Time limit per level, in seconds.
        """
        self.highscore_filename = highscore_filename
        self.levels = levels
        self.lives = lives
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost
        self.level_max_time = level_max_time


class Player:
    """Tracks the player's position, spawn point, and remaining lives."""

    def __init__(self, x: int, y: int, lives: int):
        """Initialize the player at a given position.

        Args:
            x: Starting/current column position.
            y: Starting/current row position.
            lives: Number of lives the player has.
        """
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.direction: Optional[str] = None
        self.lives = lives


class Pacgum:
    """Represents a pacgum (dot) or super-pacgum (power pellet)."""

    def __init__(
        self, x: int, y: int, available: bool = True, super: bool = False
    ):
        """Initialize a pacgum at a given maze position.

        Args:
            x: Column position in the maze.
            y: Row position in the maze.
            available: Whether the pacgum has not yet been eaten.
            super: Whether this is a super-pacgum (power pellet).
        """
        self.x = x
        self.y = y
        self.available = available
        self.super = super


class Ghost:
    """Tracks a ghost's position, movement state, and edible status."""

    def __init__(
        self,
        x: int | float,
        y: int | float,
        name: str,
        direction: Optional[str] = None,
        tkal: bool = False,
        target: Optional[tuple[int, int]] = None,
        next: Optional[tuple[int, int]] = None,
        edible: bool = False,
        edible_ts: float = 0.0,
    ):
        """Initialize a ghost at its spawn corner.

        Args:
            x: Current column position (may be fractional mid-move).
            y: Current row position (may be fractional mid-move).
            name: The ghost's identifier/name.
            direction: Current movement direction, if any.
            tkal: Whether the ghost has been eaten and is awaiting
                respawn.
            target: The maze cell the ghost is currently heading toward.
            next: The next maze cell in the ghost's planned path.
            edible: Whether the ghost is currently edible.
            edible_ts: Timestamp at which the edible state started.
        """
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.name = name
        self.tkal = tkal
        self.target = target
        self.next = next
        self.edible = edible
        self.edible_ts = edible_ts
        self.direction = direction
