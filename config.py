class Config:
    def __init__(self, highscore_filename: str, level: list[list[int]],
                 lives: int, points_per_pacgum: int, points_per_super_pacgum: int,
                 points_per_ghost: int, level_max_time:int):

        self.highscore_filename = highscore_filename

        self.level = level

        self.lives = lives

        self.points_per_pacgum = points_per_pacgum

        self.points_per_super_pacgum = points_per_super_pacgum

        self.points_per_ghost = points_per_ghost

        self.level_max_time = level_max_time
