from mazegenerator import MazeGenerator
from models import Pacgum, Ghost

class MazeGen(MazeGenerator):
    def __init__(self, size = (15, 15), perfect = False, entry_cell = (0, 0), exit_cell = (-1, -1), seed = 0):
        super().__init__(size, perfect, entry_cell, exit_cell, seed)
        self.pacgums_nb = 0
        self.pacgums: list[Pacgum]
        self.pacgumsInit()
        self.ghosts: list[Ghost]
        self.ghostsInit()


    def pacgumsInit(self):
        self.pacgums = []
        for y in range(self._height):
            for x in range(self._width):
                if self.maze[y][x] == 15:
                    continue
                if y == 0 and x == 0:
                    self.pacgums.append(Pacgum(x, y, super=True))
                elif y == 0 and x == self._width - 1:
                    self.pacgums.append(Pacgum(x, y, super=True))
                elif y == self._height - 1 and x == 0:
                    self.pacgums.append(Pacgum(x, y, super=True))
                elif y == self._height - 1 and x == self._width - 1:
                    self.pacgums.append(Pacgum(x, y, super=True))
                else:
                    self.pacgums.append(Pacgum(x, y))
                self.pacgums_nb += 1

    def ghostsInit(self):
        self.ghosts = []
        self.ghosts.append(Ghost(0, 0))
        self.ghosts.append(Ghost(self._width - 1, 0))
        self.ghosts.append(Ghost(0, self._height - 1))
        self.ghosts.append(Ghost(self._width - 1, self._height - 1))
