import pygame
import time

from engine import Engine
from models import Ghost, Pacgum, Player
from .game_state import GameState
from webcolors import name_to_rgb

CELL_SIZE = 50
SCORE_COLOR = name_to_rgb('white')
WALL_COLOR = name_to_rgb('white')
PACGUM_COLOR = name_to_rgb('gray')
SUPER_PACGUM_COLOR = name_to_rgb('gold')
PACMAN_COLOR = name_to_rgb('yellow')



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
            screen: pygame.Surface,
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

    def draw_maze(self, screen: pygame.Surface) -> None:
        for row in range(len(self.maze_directions)):
            for col in range(len(self.maze_directions[row])):
                self.draw_cell(screen, row, col, self.maze_directions[row][col] )


class PacgumRenderer:
    def __init__(self, pacgums: list[Pacgum], offset_x: float, offset_y: float):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.pacgums = pacgums

    def draw_pacgums(self, screen: pygame.Surface) -> None:
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

    def draw_player(self, screen: pygame.Surface) -> None:
        center_x = (self.player.x * CELL_SIZE + CELL_SIZE // 2 + self.offset_x)
        center_y = (self.player.y * CELL_SIZE + CELL_SIZE // 2 + self.offset_y)
        pygame.draw.circle(screen, PACMAN_COLOR, (center_x, center_y), 15)


class GhostRenderer:
    def __init__(self, ghosts: list[Ghost], offset_x:float, offset_y:float):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.ghosts = ghosts

    def draw_ghosts(self, screen:pygame.Surface):
#                                                                                   hna bdelt chwiya
        for ghost in self.ghosts:
            center_x = (ghost.x * CELL_SIZE) + CELL_SIZE // 2 + self.offset_x
            center_y = (ghost.y * CELL_SIZE) + CELL_SIZE // 2 + self.offset_y
            if ghost.tkal:
                pygame.draw.circle(screen, name_to_rgb('green'), (center_x, center_y), 6)
            elif ghost.edible:
                pygame.draw.circle(screen, name_to_rgb('blue'), (center_x, center_y), 9)
            elif ghost.name == "Blinky":
                pygame.draw.circle(screen, name_to_rgb('red'), (center_x, center_y), 9)
            elif ghost.name == "Pinky":
                pygame.draw.circle(screen, name_to_rgb('pink'), (center_x, center_y), 9)
            elif ghost.name == "Inky":
                pygame.draw.circle(screen, name_to_rgb('cyan'), (center_x, center_y), 9)
            elif ghost.name == "Clyde":
                pygame.draw.circle(screen, name_to_rgb('orange'), (center_x, center_y), 9)


class PlayingState(GameState):
    def __init__(self, engine: Engine, screen: pygame.Surface, fps: int = 10):
        self.font = pygame.font.Font(None, 36)
        self.level_start = time.time()
        self.total_paused = 0
        self.pause_start = None

        self.direction = None
        self.next_direction = None
        self.player_speed = round(2 / fps, 4)

        self.engine = engine
        self.mazegen = self.engine.maze
        self.screen = screen

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

        self.ghost_renderer =  GhostRenderer(
            self.mazegen.ghosts,
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
        self.ghost_renderer =  GhostRenderer(
            self.mazegen.ghosts,
            self.offset_x,
            self.offset_y
            )
        self.player_renderer.offset_x = self.offset_x
        self.player_renderer.offset_y = self.offset_y

    def update(self):
            elapsed = time.time() - self.level_start - self.total_paused
            if elapsed > self.engine.level_max_time:
                return ('gameover', self.engine.score)

            if not self.engine.player.lives:
                return ('gameover', self.engine.score)

            self.move_player()
            result = self.engine.update()
            if result == 'tkal':
                self.direction = None

            if self.engine.maze.pacgums_nb == 0:
                self.direction = None
                if not self.engine.start_next_level():
                    return ('victory', self.engine.score)

                self.update_renderers()
                self.level_start = time.time()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
#                                                                                 wtahna bedlt chwiya
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.direction = None
                    self.engine.maze.pacgums_nb = 0
                if event.key == pygame.K_0:
                    self.engine.invincibility = not self.engine.invincibility
                if event.key == pygame.K_1:
                    self.engine.ghosts_freeze = not self.engine.ghosts_freeze
                if event.key == pygame.K_ESCAPE:
                    return 'pause'
                if event.key in {pygame.K_UP, pygame.K_w}:
                    self.next_direction = "up"
                    self.engine.player.direction = "up"
                elif event.key in {pygame.K_DOWN, pygame.K_s}:
                    self.next_direction = "down"
                    self.engine.player.direction = "down"
                elif event.key in {pygame.K_LEFT, pygame.K_a}:
                    self.next_direction = "left"
                    self.engine.player.direction = "left"
                elif event.key in {pygame.K_RIGHT, pygame.K_d}:
                    self.next_direction = "right"
                    self.engine.player.direction = "right"

    def render(self, screen:pygame.Surface):
        screen.fill((0, 0, 0))

        self.maze_renderer.draw_maze(screen)
        self.pacgum_renderer.draw_pacgums(screen)
        self.ghost_renderer.draw_ghosts(screen)
        self.player_renderer.draw_player(screen)

        self.draw_score(screen)
        self.draw_time(screen)
        self.draw_lives(screen)

    def move_player(self):
        x = self.engine.player.x
        y = self.engine.player.y
        maze = self.engine.maze.maze

        if self.engine.player.x % 1 == 0 and self.engine.player.y % 1 == 0:
            self.engine.player.x = int(self.engine.player.x)
            self.engine.player.y = int(self.engine.player.y)
        if self.next_direction and self.can_move(x, y, self.next_direction, maze):
            self.direction = self.next_direction
            self.next_direction = None

        if self.direction and self.can_move(x, y, self.direction, maze):
            if self.direction == "up":
                self.engine.player.y = round(self.engine.player.y - self.player_speed, 4)
            elif self.direction == "down":
                self.engine.player.y = round(self.engine.player.y + self.player_speed, 4)
            elif self.direction == "left":
                self.engine.player.x = round(self.engine.player.x - self.player_speed, 4)
            elif self.direction == "right":
                self.engine.player.x = round(self.engine.player.x + self.player_speed, 4)

    def can_move(self, x, y, direction, maze):
        if x % 1 != 0 or y % 1 != 0:
            return direction == self.direction
        xi, yi = int(x), int(y)
        if direction == "up":
            return yi > 0 and not (maze[yi][xi] & 1)
        if direction == "down":
            return yi < len(maze) - 1 and not (maze[yi][xi] & 4)
        if direction == "left":
            return xi > 0 and not (maze[yi][xi] & 8)
        if direction == "right":
            return xi < len(maze[yi]) - 1 and not (maze[yi][xi] & 2)
        return False

    def draw_score(self, screen: pygame.Surface):
        score_text = self.font.render(
            f"Score: {self.engine.score}",
            True,
            SCORE_COLOR
        )

        screen.blit(score_text, (20, 20))

    def draw_time(self, screen: pygame.Surface):
        elapsed = time.time() - self.level_start - self.total_paused
        remaining = max(0, self.engine.level_max_time - elapsed)
        time_text = self.font.render(f"Time: {int(remaining)}", True, SCORE_COLOR)
        screen.blit(time_text, (20, 50))

    def draw_lives(self, screen: pygame.Surface):
        lives_text = self.font.render(
            f"Lives: {self.engine.player.lives}/{self.engine.lives}",
            True,
            SCORE_COLOR
        )
        screen.blit(lives_text, (300, 20))
