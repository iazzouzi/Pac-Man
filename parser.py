"""Configuration parsing and validation utilities.

This module handles loading a JSON configuration file (with support for
``#`` and ``//`` style comments), validating its contents, and producing
a :class:`Config` object with safe defaults applied whenever a value is
missing or invalid.
"""

import json
import os
import sys

from models import Config


class Parser:
    """Load, sanitize, and validate the game configuration file."""

    @staticmethod
    def filePreprocess(file: str) -> None:
        """Strip comment lines from a JSON config file in place.

        Lines containing ``#`` or ``//`` are treated as comments and
        removed before the file is parsed as JSON.

        Args:
            file: Path to the configuration file to preprocess.

        Raises:
            SystemExit: If the file does not have a ``.json`` extension,
                or if it cannot be read/written.
        """
        if not file.endswith('.json'):
            raise SystemExit("Error: File must be a .json file")
        try:
            with open(file) as infile, open('temp.json', 'w') as outfile:
                for line in infile:
                    if line.count('#') or line.count('//'):
                        continue
                    outfile.write(line)
            os.replace('temp.json', file)
        except OSError as e:
            raise SystemExit(e)
        except Exception as e:
            raise SystemExit(e)

    @staticmethod
    def configInit() -> Config:
        """Build a :class:`Config` populated with default values.

        Returns:
            A ``Config`` instance with the default highscore filename,
            level dimensions, lives, scoring, and time limit values.
        """
        levels = [[17, 16], [18, 16], [19, 16], [20, 16], [21, 16],
                  [22, 16], [23, 16], [24, 16], [25, 16], [26, 16]]
        config = Config("highscore.json", levels, 3, 10, 50, 200, 900.0)
        return config

    @staticmethod
    def configSetter() -> Config:
        """Parse command-line arguments and build the validated config.

        Reads the config file path from ``sys.argv``, strips comments,
        parses it as JSON, and overrides the default config values with
        any valid values found in the file. Invalid or out-of-range
        values are reported and left at their default.

        Returns:
            The resulting ``Config`` instance.

        Raises:
            SystemExit: If the argument count is wrong, the file is
                missing/unreadable, or the JSON is malformed.
        """
        if len(sys.argv) != 2:
            raise SystemExit("Error: Invalid number of arguments")
        file = sys.argv[1]
        Parser.filePreprocess(file)
        try:
            with open(file) as infile:
                data = json.load(infile)
        except json.JSONDecodeError as e:
            raise SystemExit(e)
        config = Parser.configInit()

        if "highscore_filename" in data:
            highscore_filename = data["highscore_filename"]
            if not highscore_filename:
                print("Error: Highscore filename cannot be empty")
            elif not highscore_filename.endswith('.json'):
                print("Error: Highscore file must be a .json file")
            else:
                config.highscore_filename = highscore_filename

        if "levels" in data:
            levels = data["levels"]
            if not levels:
                print("Error: Level cannot be empty")
            elif len(levels) < 10:
                print("Error: Level must contain 10 levels or more")
            elif isinstance(levels, list) and all(
                isinstance(lvl, list) and len(lvl) == 2 for lvl in levels
            ):
                for width, height in levels:
                    if not isinstance(width, int) or not isinstance(
                        height, int
                    ):
                        print("Error: Level dimensions must be integers")
                        break
                    if (
                        width < 16 or width > 38
                        or height < 16 or height > 18
                    ):
                        print(
                            "Error: Level dimensions must be between "
                            "16 and 38 for width and between 16 and 18 "
                            "for height"
                        )
                        break
                else:
                    config.levels = levels
            else:
                print("Error: Level must be a list of lists of two integers")

        if "lives" in data:
            lives = data["lives"]
            if not lives:
                print("Error: Lives cannot be empty")
            elif isinstance(lives, int) and 0 < lives <= 15:
                config.lives = lives
            else:
                print(
                    "Error: Lives must be a positive integer between 1 and 15"
                )

        if "points_per_pacgum" in data:
            points_per_pacgum = data["points_per_pacgum"]
            if not points_per_pacgum:
                print("Error: Points per pacgum cannot be empty")
            elif (
                isinstance(points_per_pacgum, int)
                and 0 < points_per_pacgum <= 1000
            ):
                config.points_per_pacgum = points_per_pacgum
            else:
                print(
                    "Error: Points per pacgum must be a positive integer "
                    "between 1 and 1000"
                )

        if "points_per_super_pacgum" in data:
            points_per_super_pacgum = data["points_per_super_pacgum"]
            if not points_per_super_pacgum:
                print("Error: Points per super pacgum cannot be empty")
            elif (
                isinstance(points_per_super_pacgum, int)
                and 0 < points_per_super_pacgum <= 1000
            ):
                config.points_per_super_pacgum = points_per_super_pacgum
            else:
                print(
                    "Error: Points per super pacgum must be a positive "
                    "integer between 1 and 1000"
                )

        if "points_per_ghost" in data:
            points_per_ghost = data["points_per_ghost"]
            if not points_per_ghost:
                print("Error: Points per ghost cannot be empty")
            elif (
                isinstance(points_per_ghost, int)
                and 0 < points_per_ghost <= 1000
            ):
                config.points_per_ghost = points_per_ghost
            else:
                print(
                    "Error: Points per ghost must be a positive integer "
                    "between 1 and 1000"
                )

        if "level_max_time" in data:
            level_max_time = data["level_max_time"]
            if not level_max_time:
                print("Error: Level max time cannot be empty")
            elif (
                isinstance(level_max_time, float | int)
                and 0 < level_max_time <= 1200
            ):
                config.level_max_time = level_max_time
            else:
                print(
                    "Error: Level max time must be a positive float"
                    " or integer between 0 and 1200"
                )

        return config
