class Config:
    def __init__(self, highscore_filename: str, levels: list[list[int]],
                 lives: int, points_per_pacgum: int, points_per_super_pacgum: int,
                 points_per_ghost: int, level_max_time: float):

        self.highscore_filename = highscore_filename

        self.levels = levels

        self.lives = lives

        self.points_per_pacgum = points_per_pacgum

        self.points_per_super_pacgum = points_per_super_pacgum

        self.points_per_ghost = points_per_ghost

        self.level_max_time = level_max_time

class Player:
    def __init__(self, x: int, y: int, lives: int):
        self.x = x
        self.y = y
        self.lives = lives

class Pacgum:
    def __init__(self, x: int, y: int, available: bool = True, super: bool = False):
        self.x = x
        self.y = y
        self.available = available
        self.super = super

class Ghost:
    def __init__(self, x: int, y: int, edible: bool = False, edible_ts: float = 0.0,
                 available: bool = True, available_ts: float = 0.0):
        self.x = x
        self.y = y
        self.edible = edible
        self.edible_ts = edible_ts
        self.available = available
        self.available_ts = available_ts
