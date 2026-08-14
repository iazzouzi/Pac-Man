class Ghost:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.edible = False
        self.edible_ts = 0.0
        self.available = True
        self.available_ts = 0.0
