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

        self.invincibility = False

        self.ghost_freeze = False

    def initialize_level(self, level):
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

            if ghost.available and self.player.x == int(ghost.x) and self.player.y == int(ghost.y):
                if ghost.edible:
                    self.score += self.points_per_ghost
                    ghost.x = ghost.base_x
                    ghost.y = ghost.base_y
                    ghost.available = False
                    ghost.available_ts = time.time()
                elif not self.invincibility:
                    self.player.lives -= 1
                    self.player.x = self.player.base_x
                    self.player.y = self.player.base_y
                    for gh in self.maze.ghosts:
                        gh.x = gh.base_x
                        gh.y = gh.base_y
                    return 'tkal'
            if self.ghost_freeze:
                continue
            if ghost.available and ghost.x % 1 == 0 and ghost.y % 1 == 0:
                if ghost.edible:
                    if self.player.x < self.maze._width // 2 and self.player.y < self.maze._height // 2:
                        (x, y) = (self.maze._width - 1, self.maze._height - 1)
                    elif self.player.x > self.maze._width // 2 and self.player.y > self.maze._height // 2:
                        (x, y) = (0, 0)
                    elif self.player.x < self.maze._width // 2 and self.player.y > self.maze._height // 2:
                        (x, y) = (self.maze._width - 1, 0)
                    else:
                        (x, y) = (0, self.maze._height - 1)
                    ghost.target = next(self.maze.maze, (int(ghost.x), int(ghost.y)), (x, y))
                else:
                    ghost.target = next(self.maze.maze, (int(ghost.x), int(ghost.y)), (self.player.x, self.player.y))
            if ghost.available and ghost.target is not None:
                if ghost.x < ghost.target[0]:
                    ghost.x = round(ghost.x + 0.2, 1)
                elif ghost.x > ghost.target[0]:
                    ghost.x = round(ghost.x - 0.2, 1)

                if ghost.y < ghost.target[1]:
                    ghost.y = round(ghost.y + 0.2, 1)
                elif ghost.y > ghost.target[1]:
                    ghost.y = round(ghost.y - 0.2, 1)

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
                json.dump(sorted(data, key=lambda x: (x["score"], x["name"]), reverse=True), file)
        except (OSError, Exception) as e:
            print(f"Error occurred while writing to highscore file: {e}")

    def top_scores(self) -> dict[str, int]:
        loaded = {}
        file = self.highscore_filename
        with open(file, 'r') as f:
            data = json.load(f)
        for dict_ in data:
            loaded[dict_['name']] = dict_['score']
        return {key: loaded[key] for key in list(loaded)[:5]}

