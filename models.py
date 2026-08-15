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
