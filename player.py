class Player:
    def __init__(self, x: int = 0, y: int = 0, lives: int = 0, temp_power: bool = False):
        self.x = x
        self.y = y
        self.lives = lives
        self.temp_power = temp_power
