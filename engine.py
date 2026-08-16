import json
import time
from algo import next
from typing import Any
from models import Config, Player
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

        self.player = Player(0, 0, lives=self.lives)

    def gameLoop(self):
        score = 0
        break_loop = False
        for level in self.levels:
            if break_loop:
                break
            try:
                maze = MazeGen((level[0], level[1]))
            except Exception as e:
                raise SystemExit(e)
            x = level[0] // 2
            y = level[1] // 2
            while maze.maze[y][x] == 15:
                x -= 1
            for pacgum in maze.pacgums:
                if pacgum.x == x and pacgum.y == y:
                    pacgum.available = False
            self.player.x = x
            self.player.y = y
            start = time.time()
            while maze.pacgums_nb:
                if time.time() - start > self.level_max_time:
                    break_loop = True
                    break
                if not self.player.lives:
                    break_loop = True
                    break
                for ghost in maze.ghosts:
                    if not ghost.available:
                        if time.time() - ghost.available_ts > 10:
                            ghost.available = True
                    if ghost.edible:
                        if time.time() - ghost.edible_ts > 10:
                            ghost.edible = False
                    if ghost.available and self.player.x == ghost.x and self.player.y == ghost.y:
                        if ghost.edible:
                            score += self.points_per_ghost
                            ghost.available = False
                            ghost.available_ts = time.time()
                        else:
                            self.player.lives -= 1
                    # if ghost.available:
                    #     nxt = next(maze.maze, (ghost.x, ghost.y), (self.player.x, self.player.y))
                    #     if nxt:
                    #         ghost.x = nxt[0]
                    #         ghost.y = nxt[1]
                for pacgum in maze.pacgums:
                    if pacgum.available and self.player.x == pacgum.x and self.player.y == pacgum.y:
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

