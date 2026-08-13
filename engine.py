import json
from config import Config
from player import Player
from mazegen import MazeGen
from typing import Any

class Engine:
    def __init__(self, config: Config):

        self.highscore_filename = config.highscore_filename

        self.level = config.level

        self.lives = config.lives

        self.points_per_pacgum = config.points_per_pacgum

        self.points_per_super_pacgum = config.points_per_super_pacgum

        self.points_per_ghost = config.points_per_ghost

        self.level_max_time = config.level_max_time

    def gameLoop(self):
        break_loop = False
        for level in self.level:
            if break_loop:
                break
            try:
                maze = MazeGen((level[0], level[1]))
            except Exception as e:
                raise SystemExit(e)
            player = Player(level[0] / 2, level[1] / 2, self.lives)
            while (maze.pacgums + maze.super_pacgums) > 0:
                if not player.lives:
                    break_loop = True
                    break

    def highscores_caching(self, name: str, score: int):
        data: list[dict[str, Any]] = []
        try:
            with open(self.highscore_filename, "r") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError, Exception):
            pass
        try:
            with open(self.highscore_filename, "w") as file:
                data.append({"name": name, "score": score})
                json.dump(data, file)
        except (OSError, Exception) as e:
            print(f"Error occurred while writing to highscore file: {e}")

