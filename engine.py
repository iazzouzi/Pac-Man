from mazegenerator import MazeGenerator
from config import Config

class Engine:
    def __init__(self, config: Config):

        self.highscore_filename = config.highscore_filename

        self.level = config.level

        self.lives = config.lives

        self.points_per_pacgum = config.points_per_pacgum

        self.points_per_super_pacgum = config.points_per_super_pacgum

        self.points_per_ghost = config.points_per_ghost

        self.level_max_time = config.level_max_time

    