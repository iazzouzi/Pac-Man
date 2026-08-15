import pygame
import webcolors
from mazegen import MazeGen

CELL_SIZE = 50
WALL_COLOR = webcolors.name_to_rgb('white')
maze_gen = MazeGen((20,15))

class MazeRenderer:
    def __init__(self, maze:list[list[int]]):
        self.maze = maze
        self.maze_directions = self.maze_to_directions()


    def maze_to_directions(self) -> list[list[dict[str, bool]]]:
        cells_directions = []
        for row in self.maze:
            row_maze = []
            for col in row:
                row_maze.append(
                    {
                        "N": bool(col & 1),
                        "E": bool(col & 2), 
                        "S": bool(col & 4),
                        "W": bool(col & 8) 
                    }
                    )
            cells_directions.append(row_maze)
        return cells_directions


    def draw_cell(
            self,
            screen: pygame.surface,
            row: int,
            col: int,
            cell: dict[str, bool]
            ) -> None:

        x = col * CELL_SIZE
        y = row * CELL_SIZE
        if cell['N']:
            pygame.draw.line(screen, WALL_COLOR,
                            (x, y),
                            (x + CELL_SIZE, y),
                            3)
        if cell['E']:
            pygame.draw.line(screen, WALL_COLOR,
                            (x + CELL_SIZE, y),
                            (x + CELL_SIZE, y + CELL_SIZE),
                            3)
        if cell['S']:
            pygame.draw.line(screen, WALL_COLOR,
                            (x, y + CELL_SIZE),
                            (x + CELL_SIZE, y + CELL_SIZE),
                            3)
        if cell['W']:
            pygame.draw.line(screen, WALL_COLOR,
                            (x, y),
                            (x, y + CELL_SIZE),
                            3)


    def draw_maze(self, screen: pygame.surface) -> None:
        for row in range(len(self.maze_directions)):
            for col in range(len(self.maze_directions[row])):
                self.draw_cell(screen, row + 1, col + 1, self.maze_directions[row][col] )


class GameScreen:
    def __init__(self, maze: list[list[int]]):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Pacman")
        self.running =  True
        self.maze = maze
        self.maze_renderer = MazeRenderer(self.maze)
    def run(self):
        while self.running:
            self.handle_events()
            self.render()
        print("Game closed")
        pygame.quit()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    def render(self):
        self.maze_renderer.draw_maze(self.screen)
        pygame.display.flip()


game = GameScreen(maze_gen.maze)
game.run()