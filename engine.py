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

        self.maze = None

        self.score = 0

        self.current_level = 0

        self.base_x = 0

        self.base_y = 0

    def initialize_level(self, level):
        try:
            self.maze = MazeGen((level[0], level[1]))
        except Exception as e:
            raise SystemExit(e)

        self.base_x = level[0] // 2
        self.base_y = level[1] // 2

        while self.maze.maze[self.base_y][self.base_x] == 15:
            self.base_x -= 1

        for pacgum in self.maze.pacgums:
            if pacgum.x == self.base_x and pacgum.y == self.base_y:
                pacgum.available = False
                self.maze.pacgums_nb -= 1

        self.player.x = self.base_x
        self.player.y = self.base_y

    def start_next_level(self):
        if self.current_level >= len(self.levels):
            return False
        self.initialize_level(self.levels[self.current_level])
        self.current_level += 1
        return True

    def update(self):
        for ghost in self.maze.ghosts:
            if not ghost.available:
                if time.time() - ghost.available_ts > 10.0:
                    ghost.available = True

            if ghost.edible:
                if time.time() - ghost.edible_ts > 10.0:
                    ghost.edible = False

            if ghost.available and self.player.x == ghost.x and self.player.y == ghost.y:
                if ghost.edible:
                    self.score += self.points_per_ghost
                    ghost.available = False
                    ghost.available_ts = time.time()
                else:
                    self.player.lives -= 1
                    self.player.x = self.base_x
                    self.player.y = self.base_y
            # if ghost.available:
            #     nxt = next(maze.maze, (ghost.x, ghost.y), (self.player.x, self.player.y))
            #     if nxt:
            #         ghost.x = nxt[0]
            #         ghost.y = nxt[1]
        for pacgum in self.maze.pacgums:
            if pacgum.available and self.player.x == pacgum.x and self.player.y == pacgum.y:
                if pacgum.super:
                    self.score += self.points_per_super_pacgum

                    for ghost in self.maze.ghosts:
                        ghost.edible = True
                        ghost.edible_ts = time.time()
                else:
                    self.score += self.points_per_pacgum

                pacgum.available = False
                self.maze.pacgums_nb -= 1

    @staticmethod
    def highscores_caching(name: str, score: int, highscore_filename):
        data: list[dict[str, Any]] = []
        try:
            with open(highscore_filename, "r") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError, Exception):
            pass
        try:
            with open(highscore_filename, "w") as file:
                data.append({"name": name, "score": score})
                json.dump(data, file)
        except (OSError, Exception) as e:
            print(f"Error occurred while writing to highscore file: {e}")
