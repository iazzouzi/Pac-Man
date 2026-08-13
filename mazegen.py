from mazegenerator import MazeGenerator
from pacgum import Pacgum

class MazeGen(MazeGenerator):
    def __init__(self, size = (15, 15), perfect = False, entry_cell = (0, 0), exit_cell = (-1, -1), seed = 0):
        super().__init__(size, perfect, entry_cell, exit_cell, seed)
        self.pacgums: list[Pacgum]
        self.pacgums_nb = size[0] * size[1] - 1
        self.pacgumsInit()

    def pacgumsInit(self):
        self.pacgums = []
        for y in range(self._height):
            for x in range(self._width):
                if y != self._height / 2 and x != self._width / 2:
                    self.pacgums.append(Pacgum(x, y))
        