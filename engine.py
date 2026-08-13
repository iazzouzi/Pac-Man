from config import Config
from player import Player
from mazegen import MazeGen

class Engine:
    def __init__(self, config: Config):

        self.highscore_filename = config.highscore_filename

        self.level = config.level

        self.lives = config.lives

        self.points_per_pacgum = config.points_per_pacgum

        self.points_per_super_pacgum = config.points_per_super_pacgum

        self.points_per_ghost = config.points_per_ghost

        self.level_max_time = config.level_max_time

    def gameLoop(self):
        break_loop = False
        for level in self.level:
            if break_loop:
                break
            try:
                maze = MazeGen((level[0], level[1]))
            except Exception as e:
                raise SystemExit(e)
            player = Player(level[0] / 2, level[1] / 2, self.lives)
            while (maze.pacgums + maze.super_pacgums) > 0 :
                if not player.lives:
                    break_loop = True
                    break
                # zid condition 3la 7sab time ila sala time rah machi game over b7al lives yked restarti fnfss level
