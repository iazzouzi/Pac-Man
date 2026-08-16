import pygame
import webcolors
from engine import Engine
from parser import Parser
from models import Pacgum, Player

CELL_SIZE = 50
SCORE_COLOR = webcolors.name_to_rgb('white')
WALL_COLOR = webcolors.name_to_rgb('white')
PACGUM_COLOR = webcolors.name_to_rgb('gray')
SUPER_PACGUM_COLOR = webcolors.name_to_rgb('gold')
PACMAN_COLOR = webcolors.name_to_rgb('yellow')


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


class PlayerRenderer:
    def __init__(self, player: Player, offset_x, offset_y):
        self.player = player
        self.offset_x = offset_x
        self.offset_y = offset_y
    def draw_player(self, screen: pygame.surface) -> None:
        center_x = (self.player.x * CELL_SIZE + CELL_SIZE // 2 + self.offset_x)
        center_y = (self.player.y * CELL_SIZE + CELL_SIZE // 2 + self.offset_y)
        pygame.draw.circle(screen, PACMAN_COLOR, (center_x, center_y), 15)


class GameScreen:
    def __init__(self, engine: Engine):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Pacman")
        self.running = True
        self.font = pygame.font.Font(None, 36)

        self.engine = engine
        self.mazegen = self.engine.maze

        self.maze_width = len(self.mazegen.maze[0]) * CELL_SIZE
        self.maze_height = len(self.mazegen.maze) * CELL_SIZE

        screen_width, screen_height = self.screen.get_size()

        self.offset_x = (screen_width - self.maze_width) / 2
        self.offset_y = (screen_height - self.maze_height) / 2

        self.maze_renderer = MazeRenderer(
            self.mazegen.maze,
            self.offset_x,
            self.offset_y
        )

        self.pacgum_renderer = PacgumRenderer(
            self.mazegen.pacgums,
            self.offset_x,
            self.offset_y
        )

        self.player_renderer = PlayerRenderer(
            self.engine.player,
            self.offset_x,
            self.offset_y
        )

    def update_renderers(self):
        self.mazegen = self.engine.maze

        self.maze_width = len(self.mazegen.maze[0]) * CELL_SIZE
        self.maze_height = len(self.mazegen.maze) * CELL_SIZE

        self.offset_x = (self.screen.get_width() - self.maze_width) / 2
        self.offset_y = (self.screen.get_height() - self.maze_height) / 2

        self.maze_renderer = MazeRenderer(
            self.mazegen.maze,
            self.offset_x,
            self.offset_y
        )

        self.pacgum_renderer = PacgumRenderer(
            self.mazegen.pacgums,
            self.offset_x,
            self.offset_y
        )
        self.player_renderer.offset_x = self.offset_x
        self.player_renderer.offset_y = self.offset_y

    def run(self):
        while self.running:
            self.handle_events()
            self.engine.update()
            if self.engine.maze.pacgums_nb == 0:
                if not self.engine.start_next_level():
                    self.running = False
                    continue

                self.update_renderers()
            self.render()
        pygame.quit()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                x = self.engine.player.x
                y = self.engine.player.y
                if event.key == pygame.K_SPACE:
                    self.engine.maze.pacgums_nb = 0
                if event.key == pygame.K_UP and y > 0 and not (self.engine.maze.maze[y][x] & 1):
                    self.engine.player.y -= 1

                elif event.key == pygame.K_DOWN and y < len(self.engine.maze.maze) - 1 and not (self.engine.maze.maze[y][x] & 4):
                    self.engine.player.y += 1

                elif event.key == pygame.K_LEFT and x > 0 and not (self.engine.maze.maze[y][x] & 8):
                    self.engine.player.x -= 1

                elif event.key == pygame.K_RIGHT and x < len(self.engine.maze.maze[y]) - 1 and not (self.engine.maze.maze[y][x] & 2):
                    self.engine.player.x += 1
    def render(self):
        self.screen.fill((0, 0, 0))

        self.maze_renderer.draw_maze(self.screen)
        self.pacgum_renderer.draw_pacgums(self.screen)
        self.player_renderer.draw_player(self.screen)

        self.draw_score()

        pygame.display.flip()
    def draw_score(self):
        score_text = self.font.render(
            f"Score: {self.engine.score}",
            True,
            SCORE_COLOR
        )

        self.screen.blit(score_text, (20, 20))
