import pygame
import webcolors
from mazegen import MazeGen
from models import Pacgum

CELL_SIZE = 50
WALL_COLOR = webcolors.name_to_rgb('white')
PACGUM_COLOR = webcolors.name_to_rgb('gray')
SUPER_PACGUM_COLOR = webcolors.name_to_rgb('gold')


class MazeRenderer:
    def __init__(self, maze:list[list[int]], offset_x: float, offset_y: float):
        self.maze = maze
        self.offset_x = offset_x
        self.offset_y = offset_y
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

        x = col * CELL_SIZE + self.offset_x
        y = row * CELL_SIZE + self.offset_y
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
                self.draw_cell(screen, row, col, self.maze_directions[row][col] )


class PacgumRenderer:
    def __init__(self, pacgums: list[Pacgum], offset_x: float, offset_y: float):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.pacgums = pacgums


    def draw_pacgums(self, screen: pygame.surface) -> None:
        for pacgum in self.pacgums:
            if not pacgum.available:
                continue

            center_x = (pacgum.x * CELL_SIZE) + CELL_SIZE // 2 + self.offset_x
            center_y = (pacgum.y * CELL_SIZE) + CELL_SIZE // 2 + self.offset_y
            if pacgum.super:
                pygame.draw.circle(screen, SUPER_PACGUM_COLOR, (center_x, center_y), 7)
            else:
                pygame.draw.circle(screen, PACGUM_COLOR, (center_x, center_y), 3)


class GameScreen:
    def __init__(self, mazegen: MazeGen):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Pacman")
        self.running =  True

        self.mazegen = mazegen

        self.maze_width = len(maze_gen.maze[0]) * CELL_SIZE
        self.maze_height = len(maze_gen.maze) * CELL_SIZE

        screen_width, screen_height = self.screen.get_size()

        self.offset_x = (screen_width  - self.maze_width)  / 2
        self.offset_y = (screen_height - self.maze_height) / 2

        self.maze_renderer = MazeRenderer(self.mazegen.maze, self.offset_x, self.offset_y)
        self.pacgum_renderer = PacgumRenderer(self.mazegen.pacgums, self.offset_x, self.offset_y)
    def run(self):
        while self.running:
            self.handle_events()
            self.render()
        pygame.quit()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    def render(self):
        self.maze_renderer.draw_maze(self.screen)
        self.pacgum_renderer.draw_pacgums(self.screen)
        pygame.display.flip()


maze_gen = MazeGen((20,15))
game = GameScreen(maze_gen)
game.run()