import json
import time
from typing import Any
from player import Player
from config import Config
from mazegen import MazeGen

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
        score = 0
        break_loop = False
        player = Player(lives=self.lives)
        for level in self.level:
            if break_loop:
                break
            try:
                maze = MazeGen((level[0], level[1]))
            except Exception as e:
                raise SystemExit(e)
            player.x = level[0] / 2
            player.y = level[1] / 2
            start = time.time()
            while maze.pacgums_nb:
                if time.time() - start > self.level_max_time:
                    break_loop = True
                    break
                if not player.lives:
                    break_loop = True
                    break
                for ghost in maze.ghosts:
                    if player.x == ghost.x and player.y == ghost.y:
                        player.lives -= 1
                for pacgum in maze.pacgums:
                    if player.x == pacgum.x and player.y == pacgum.y:
                        if pacgum.super:
                            score += self.points_per_super_pacgum
                        else:
                            score += self.points_per_pacgum
                        pacgum.available = False
                        maze.pacgums_nb -= 1

        self.highscores_caching("Test", score)

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

