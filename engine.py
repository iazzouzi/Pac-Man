import json
import time
from typing import Any
from models import Player
from config import Config
from mazegen import MazeGen

class Engine:
    def __init__(self, config: Config):

        self.highscore_filename = config.highscore_filename

        self.levels = config.levels

        self.lives = config.lives

        self.points_per_pacgum = config.points_per_pacgum

        self.points_per_super_pacgum = config.points_per_super_pacgum

        self.points_per_ghost = config.points_per_ghost

        self.level_max_time = config.level_max_time

    def gameLoop(self):
        score = 0
        break_loop = False
        player = Player(0, 0, lives=self.lives)
        for level in self.levels:
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
                    if not ghost.available:
                        if time.time() - ghost.available_ts > 10:
                            ghost.available = True
                    if ghost.edible:
                        if time.time() - ghost.edible_ts > 10:
                            ghost.edible = False
                    if player.x == ghost.x and player.y == ghost.y:
                        if ghost.edible:
                            score += self.points_per_ghost
                            ghost.available = False
                            ghost.available_ts = time.time()
                        else:
                            player.lives -= 1
                for pacgum in maze.pacgums:
                    if player.x == pacgum.x and player.y == pacgum.y:
                        if pacgum.super:
                            score += self.points_per_super_pacgum
                            for ghost in maze.ghosts:
                                ghost.edible = True
                                ghost.edible.ts = time.time()
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

