class Player:
    def __init__(self, x: int, y: int, lives: int, temp_power: bool = False):
        self.x = x
        self.y = y
        self.lives = lives
        self.temp_power = temp_power
