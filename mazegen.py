from mazegenerator import MazeGenerator

class MazeGen(MazeGenerator):
    def __init__(self, size = (15, 15), perfect = False, entry_cell = (0, 0), exit_cell = (-1, -1), seed = 0):
        super().__init__(size, perfect, entry_cell, exit_cell, seed)