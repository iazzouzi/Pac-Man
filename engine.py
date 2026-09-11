import json
import time
from algo import next
from typing import Any
from models import Config, Player, Pacgum, Ghost
from mazegen import MazeGen
from time import sleep

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

        self.ghosts_freeze = False

        self.pacgum_sound = None

        self.fail_sound = None

        self.eating_ghost_sound = None

        self.return_sound = None

        self.edible_ghosts_sound = None

        self.ghosts_move_sound = None

        self.ghosts_move_sound_channel = None

        self.ready_sound = None

        self.ready_sound_channel = None

        self.ready = 0

        self.ready_ts = 0

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

    def identify_target(self, ghost: Ghost):
        if ghost.tkal:
            target = (ghost.base_x, ghost.base_y)

        elif ghost.edible:
            if self.player.x < self.maze._width // 2 and self.player.y < self.maze._height // 2:
                target = (self.maze._width - 1, self.maze._height - 1)
            elif self.player.x > self.maze._width // 2 and self.player.y > self.maze._height // 2:
                target = (0, 0)
            elif self.player.x < self.maze._width // 2 and self.player.y > self.maze._height // 2:
                target = (self.maze._width - 1, 0)
            else:
                target = (0, self.maze._height - 1)

        elif ghost.name == "Blinky":
            target = (self.player.x, self.player.y)

        elif ghost.name == "Pinky":
            if self.player.direction == "up" and self.player.y - 2 >= 0 and self.player.x - 2 >= 0:
                target = (self.player.x - 2, self.player.y - 2)
            elif self.player.direction == "down" and self.player.y + 2 <= self.maze._height - 1:
                target = (self.player.x, self.player.y + 2)
            elif self.player.direction == "left" and self.player.x - 2 >= 0:
                target = (self.player.x - 2 , self.player.y)
            elif self.player.direction == "right" and self.player.x + 2 <= self.maze._width - 1:
                target = (self.player.x + 2, self.player.y)
            else:
                target = (self.player.x, self.player.y)

        elif ghost.name == "Inky":
            for gh in self.maze.ghosts:
                if gh.name == "Blinky":
                    dx = self.player.x - int(gh.x)
                    dy = self.player.y - int(gh.y)
                    if 0 <= self.player.x + dx <= self.maze._width - 1 and 0 <= self.player.y + dy <= self.maze._height - 1:
                        x = self.player.x + dx
                        y = self.player.y + dy
                    else:
                        x = self.player.x
                        y = self.player.y
            target = (x, y)

        elif ghost.name == "Clyde":
            if self.player.y - 2 >= 0 and self.player.x - 2 >= 0:
                target = (self.player.x - 2, self.player.y - 2)
            else:
                target = (self.player.x, self.player.y)

        ghost.target = next(self.maze.maze, (int(ghost.x), int(ghost.y)), target)

    def move_ghost(self, ghost: Ghost):
        if ghost.target is not None:
            target_x, target_y = ghost.target
            if ghost.tkal:
                speed = 0.2   # 6 cells/sec at 30 FPS — fast return, not Flash
            else:
                speed = 0.05
            if ghost.x < target_x:
                ghost.direction = "right"
                ghost.x = round(ghost.x + speed, 2)
            elif ghost.x > target_x:
                ghost.direction = "left"
                ghost.x = round(ghost.x - speed, 2)
            if ghost.y < target_y:
                ghost.direction = "down"
                ghost.y = round(ghost.y + speed, 2)
            elif ghost.y > target_y:
                ghost.direction = "up"
                ghost.y = round(ghost.y - speed, 2)

    def update(self):
        if not self.ready:
            if not self.ready_sound_channel or not self.ready_sound_channel.get_busy():
                self.ready_sound_channel = self.ready_sound.play()
                self.ready_ts = time.time()
        if self.ready:
            if not self.ghosts_move_sound_channel or not self.ghosts_move_sound_channel.get_busy():
                self.ghosts_move_sound_channel = self.ghosts_move_sound.play()
        if not self.ready and time.time() - self.ready_ts > 5.0:
            self.ready = 1
        if not self.ready:
            return
        for ghost in self.maze.ghosts:
            if ghost.edible:
                if time.time() - ghost.edible_ts > 10.0:
                    self.edible_ghosts_sound.fadeout(1000)
                    ghost.edible = False
            if self.ghosts_freeze:
                continue
            # if not ghost.tkal and self.player.x == int(ghost.x) and self.player.y == int(ghost.y):
            if not ghost.tkal and abs(self.player.x - ghost.x) < 0.5 and abs(self.player.y - ghost.y) < 0.5:  ##man3raf  claude li suggestaha lal9iti ma7sen fixiha
                if ghost.edible:
                    self.eating_ghost_sound.play()
                    self.score += self.points_per_ghost
                    # sleep(1.6)
                    self.return_sound.play()
                    ghost.edible = False
                    ghost.tkal = True
                    # Snap to nearest cell once so move_ghost can use sub-integer speed safely
                    ghost.x = round(ghost.x)
                    ghost.y = round(ghost.y)
                elif not self.invincibility:
                    self.ghosts_move_sound.stop()
                    self.edible_ghosts_sound.stop()
                    self.fail_sound.play()
                    self.player.lives -= 1
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
            if pacgum.available and self.player.x == pacgum.x and self.player.y == pacgum.y:
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

    def reset_after_death(self):
        self.player.x = self.player.base_x
        self.player.y = self.player.base_y
        for gh in self.maze.ghosts:
            if gh.tkal:
                continue
            gh.x = gh.base_x
            gh.y = gh.base_y

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

    def get_top_scores(self) -> dict[str, int]:
        loaded = {}
        file = self.highscore_filename
        with open(file, 'r') as f:
            data = json.load(f)
        for dict_ in data:
            loaded[dict_['name']] = dict_['score']
        return {key: loaded[key] for key in list(loaded)[:10]}

