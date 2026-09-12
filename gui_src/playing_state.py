import pygame
import time
from typing import Any
from engine import Engine
from models import Ghost, Pacgum, Player
from .game_state import GameState
from webcolors import name_to_rgb

CELL_SIZE = 50
SCORE_COLOR = name_to_rgb('white')
WALL_COLOR = (0, 0, 255)
PACGUM_COLOR = name_to_rgb('white')
SUPER_PACGUM_COLOR = name_to_rgb('gold')
PACMAN_COLOR = name_to_rgb('yellow')
ICON_COLOR = (255, 255, 255)
VALUE_COLOR = (255, 255, 0)
TIME_WARN_COLOR = (255, 60, 60)

DEATH_FRAME_DURATION = 80
DEATH_FRAME_COUNT = 16


class MazeRenderer:
    """Renders the maze grid and walls onto the screen.

    Attributes:
        maze (list[list[int]]): The maze grid data representing walls.
        offset_x (float): The horizontal offset for rendering.
        offset_y (float): The vertical offset for rendering.
        maze_directions (list[list[dict[str, bool]]]):
            Parsed directional walls.
    """
    def __init__(
            self, maze: list[list[int]],
            offset_x: float, offset_y: float):
        """Initializes the MazeRenderer.

        Args:
            maze (list[list[int]]): A 2D list containing integer values
                    for wall directions.
            offset_x (float): The horizontal offset for maze rendering.
            offset_y (float): The vertical offset for maze rendering.
        """
        self.maze = maze
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.maze_directions = self.maze_to_directions()

    def maze_to_directions(self) -> list[list[dict[str, bool]]]:
        """Converts the integer maze representation into boolean directions.

        Returns:
            list[list[dict[str, bool]]]: A 2D list indicating
                    wall presence in N, E, S, W directions.
        """
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
        """Draws a single cell of the maze.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            cell (dict[str, bool]): Dictionary of wall presences (N, E, S, W).
        """

        x = col * CELL_SIZE + self.offset_x
        y = row * CELL_SIZE + self.offset_y
        if cell['N']:
            pygame.draw.line(
                screen,
                WALL_COLOR,
                (x, y),
                (x + CELL_SIZE, y),
                3
                )
        if cell['E']:
            pygame.draw.line(
                screen,
                WALL_COLOR,
                (x + CELL_SIZE, y),
                (x + CELL_SIZE, y + CELL_SIZE),
                3
                )
        if cell['S']:
            pygame.draw.line(
                screen,
                WALL_COLOR,
                (x, y + CELL_SIZE),
                (x + CELL_SIZE, y + CELL_SIZE),
                3
                )
        if cell['W']:
            pygame.draw.line(
                screen,
                WALL_COLOR,
                (x, y),
                (x, y + CELL_SIZE),
                3
                )

    def draw_maze(self, screen: pygame.Surface) -> None:
        """Draws the entire maze.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        for row in range(len(self.maze_directions)):
            for col in range(len(self.maze_directions[row])):
                self.draw_cell(
                    screen, row, col,
                    self.maze_directions[row][col]
                )


class PacgumRenderer:
    """Renders pacgums onto the screen.

    Attributes:
        offset_x (float): The horizontal offset for rendering.
        offset_y (float): The vertical offset for rendering.
        pacgums (list[Pacgum]): List of pacgums to render.
    """
    def __init__(
            self, pacgums: list[Pacgum],
            offset_x: float, offset_y: float):
        """Initializes the PacgumRenderer.

        Args:
            pacgums (list[Pacgum]): List of pacgums to render.
            offset_x (float): The horizontal offset.
            offset_y (float): The vertical offset.
        """
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.pacgums = pacgums

    def draw_pacgums(self, screen: pygame.Surface) -> None:
        """Draws all available pacgums.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        for pacgum in self.pacgums:
            if not pacgum.available:
                continue

            center_x = (pacgum.x * CELL_SIZE) + CELL_SIZE // 2 + self.offset_x
            center_y = (pacgum.y * CELL_SIZE) + CELL_SIZE // 2 + self.offset_y
            if pacgum.super:
                pygame.draw.circle(
                    screen, SUPER_PACGUM_COLOR,
                    (center_x, center_y), 7)
            else:
                pygame.draw.circle(
                    screen, PACGUM_COLOR,
                    (center_x, center_y), 3)


class PlayerRenderer:
    """Renders the player character (Pac-Man) and animations.

    Attributes:
        player (Player): The player instance to track.
        offset_x (float): The horizontal render offset.
        offset_y (float): The vertical render offset.
        frames (dict[str, list[Any]]): Dictionary of
                        animation frames per direction.
        frame_index (int): Current frame index.
        last_frame_time (int): Last time the frame was updated.
        frame_duration (int): Duration of each frame in milliseconds.
    """
    def __init__(
        self, player: Player, offset_x: float, offset_y: float
    ) -> None:
        """Initializes the PlayerRenderer.

        Args:
            player (Player): The player instance to track.
            offset_x (float): Horizontal render offset.
            offset_y (float): Vertical render offset.
        """
        self.player = player
        self.offset_x = offset_x
        self.offset_y = offset_y

        size = (CELL_SIZE - 15, CELL_SIZE - 15)

        def load(path: str) -> Any:
            """Loads and scales an image from the given path.

            Args:
                path (str): The file path to the image.

            Returns:
                Any: The scaled pygame surface.
            """
            return pygame.transform.scale(
                pygame.image.load(path).convert_alpha(), size
            )

        base_frames = [
            load("assets/pacman_0.png"),
            load("assets/pacman_1.png"),
            load("assets/pacman_2.png"),
            load("assets/pacman_1.png"),
        ]

        def rotate(surface: Any, angle: float) -> Any:
            """Rotates a given surface by a specific angle.

            Args:
                surface (Any): The pygame surface to rotate.
                angle (float): The angle to rotate by in degrees.

            Returns:
                Any: The rotated and scaled pygame surface.
            """
            rotated = pygame.transform.rotate(surface, angle)
            return pygame.transform.scale(rotated, size)

        self.frames: dict[str, list[Any]] = {
            "right": base_frames,
            "left":  [
                pygame.transform.flip(f, True, False)
                for f in base_frames
            ],
            "up":    [rotate(f, 90) for f in base_frames],
            "down":  [rotate(f, -90) for f in base_frames],
        }

        self.frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.frame_duration = 100

    def draw_player(
            self, screen: pygame.Surface, direction: str | None
            ) -> None:
        """Draws the animated player onto the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
            direction (str | None): The movement direction, or None to
                    use the default right-facing animation.
        """
        now = pygame.time.get_ticks()
        if now - self.last_frame_time >= self.frame_duration:
            self.frame_index = (self.frame_index + 1) % 4
            self.last_frame_time = now

        direction = direction or "right"
        frame = self.frames[direction][self.frame_index]

        w, h = frame.get_size()
        x = int(
            self.player.x * CELL_SIZE
            + self.offset_x + (CELL_SIZE - w) / 2
        )
        y = int(
            self.player.y * CELL_SIZE
            + self.offset_y + (CELL_SIZE - h) / 2
        )
        self._last_draw_x = x
        self._last_draw_y = y
        screen.blit(frame, (x, y))


class DeathAnimationRenderer:
    """Renders the death animation sequence for the player.

    Attributes:
        frames (list[Any]): List of death animation frames.
        active (bool): Whether the death animation is currently playing.
        frame_index (int): The current frame index.
        last_frame_time (int): The timestamp of the last frame update.
        draw_x (int): Horizontal draw coordinate.
        draw_y (int): Vertical draw coordinate.
    """
    def __init__(self) -> None:
        """Initializes the DeathAnimationRenderer and loads its frames."""
        size = (CELL_SIZE - 15, CELL_SIZE - 15)

        def load(i: int) -> Any:
            """Loads and scales a specific death frame by index.

            Args:
                i (int): Frame index.

            Returns:
                Any: Scaled pygame surface.
            """
            return pygame.transform.scale(
                pygame.image.load(
                    f"assets/pacman_death_{i}.png"
                ).convert_alpha(), size
            )

        self.frames = [load(i) for i in range(1, DEATH_FRAME_COUNT + 1)]
        self.reset()

    def reset(self) -> None:
        """Resets the state of the death animation to inactive."""
        self.active = False
        self.frame_index = 0
        self.last_frame_time = 0
        self.draw_x = 0
        self.draw_y = 0

    def start(self, draw_x: int, draw_y: int) -> None:
        """Starts the death animation at the given coordinates.

        Args:
            draw_x (int): The x-coordinate to draw the animation.
            draw_y (int): The y-coordinate to draw the animation.
        """
        self.active = True
        self.frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.draw_x = draw_x
        self.draw_y = draw_y

    def update_and_draw(self, screen: pygame.Surface) -> bool:
        """Updates animation state and draws current frame to the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.

        Returns:
            bool: True if the animation just finished, False otherwise.
        """
        if not self.active:
            return False
        now = pygame.time.get_ticks()
        if now - self.last_frame_time >= DEATH_FRAME_DURATION:
            self.frame_index += 1
            self.last_frame_time = now
        if self.frame_index >= DEATH_FRAME_COUNT:
            self.active = False
            return True
        screen.blit(self.frames[self.frame_index], (self.draw_x, self.draw_y))
        return False


class GhostRenderer:
    """Renders the ghosts and their animations onto the screen.

    Attributes:
        ghosts (list[Ghost]): The list of ghosts to render.
        offset_x (float): The horizontal render offset.
        offset_y (float): The vertical render offset.
        frame_sets (dict[str, list[Any]]): Dictionary containing
                            animations for each ghost state.
        frame_index (dict[str, int]): Current animation frame
                        index for each state.
        last_frame_time (dict[str, int]): Timestamp of the last frame update.
        frame_duration (int): Duration of each animation frame in milliseconds.
    """
    def __init__(self, ghosts: list[Ghost], offset_x: float, offset_y: float):
        """Initializes the GhostRenderer.

        Args:
            ghosts (list[Ghost]): The list of ghosts.
            offset_x (float): Horizontal render offset.
            offset_y (float): Vertical render offset.
        """
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.ghosts = ghosts

        size = (CELL_SIZE - 17, CELL_SIZE - 17)

        def load(path: str) -> Any:
            """Loads and scales an image for ghost animation frames.

            Args:
                path (str): The file path to the image.

            Returns:
                Any: The scaled pygame surface.
            """
            return pygame.transform.scale(
                pygame.image.load(path).convert_alpha(), size
            )

        self.frame_sets = {
            "Blinky": [
                load("assets/blinky_1.png"),
                load("assets/blinky_2.png"),
            ],
            "Pinky": [
                load("assets/pinky_1.png"),
                load("assets/pinky_2.png"),
            ],
            "Inky": [
                load("assets/inky_1.png"),
                load("assets/inky_2.png"),
            ],
            "Clyde": [
                load("assets/clyde_1.png"),
                load("assets/clyde_2.png"),
            ],
            "scared": [
                load("assets/scared_1.png"),
                load("assets/scared_2.png"),
            ],
            "eyes_left":  [load("assets/eyes_2_left.png")],
            "eyes_right": [load("assets/eyes_2_right.png")],
        }

        self.frame_index = {key: 0 for key in self.frame_sets}
        self.last_frame_time = {
            key: pygame.time.get_ticks()
            for key in self.frame_sets
        }
        self.frame_duration = 150

    def _advance_frame(self, key: str) -> int:
        """Advances the animation frame for a specific ghost state.

        Args:
            key (str): The animation key corresponding to a ghost or state.

        Returns:
            int: The updated frame index.
        """
        now = pygame.time.get_ticks()
        if now - self.last_frame_time[key] >= self.frame_duration:
            self.frame_index[key] = (
                (self.frame_index[key] + 1)
                % len(self.frame_sets[key])
            )
            self.last_frame_time[key] = now
        return self.frame_index[key]

    def draw_ghosts(self, screen: pygame.Surface) -> None:
        """Draws all ghosts onto the screen with their current animation frame.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        for ghost in self.ghosts:
            blinky = self.frame_sets["Blinky"][0]
            w_offset = (
                (CELL_SIZE - blinky.get_width()) // 2
            )
            h_offset = (
                (CELL_SIZE - blinky.get_height()) // 2
            )
            x = int(ghost.x * CELL_SIZE + self.offset_x + w_offset)
            y = int(ghost.y * CELL_SIZE + self.offset_y + h_offset)

            if ghost.tkal:
                key = "eyes_left" if ghost.x > ghost.base_x else "eyes_right"
                frame = self.frame_sets[key][0]
            elif ghost.edible:
                idx = self._advance_frame("scared")
                frame = self.frame_sets["scared"][idx]
            else:
                key = ghost.name
                idx = self._advance_frame(key)
                frame = self.frame_sets[key][idx]

            screen.blit(frame, (x, y))


class HUD:
    """Renders the Heads-Up Display showing score, level, time, and lives.

    Attributes:
        engine (Engine): The main game engine instance.
        state (PlayingState): The current game state.
        font_label (pygame.font.Font): Font used for labels.
        font_value (pygame.font.Font): Font used for dynamic values.
        font_icon (pygame.font.Font): Font used for icons.
        life_full (pygame.Surface): The image representing an available life.
        life_empty (pygame.Surface): The image representing a lost life.
    """
    def __init__(self, engine: Engine, state: 'PlayingState'):
        """Initializes the HUD.

        Args:
            engine (Engine): The main game engine.
            state (PlayingState): The active playing state.
        """
        self.engine = engine
        self.state = state
        font_path = "resources/PressStart2P-Regular.ttf"
        self.font_label = pygame.font.Font(font_path, 16)
        self.font_value = pygame.font.Font(font_path, 22)
        self.font_icon = pygame.font.SysFont("dejavusans", 28)

        life_size = (50, 50)
        self.life_full = pygame.transform.scale(
            pygame.image.load("assets/pacman_1.png").convert_alpha(), life_size
        )
        self.life_empty = pygame.transform.scale(
            pygame.image.load("assets/pacman_1.png").convert_alpha(), life_size
        )

    def _draw_item(
        self, screen: pygame.Surface, icon: str, value: str, x: int, y: int
    ) -> None:
        """Draws a single HUD item with an icon and a value.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
            icon (str): The icon text to display.
            value (str): The value text to display.
            x (int): The horizontal coordinate.
            y (int): The vertical coordinate.
        """
        icon_surf = self.font_icon.render(icon, True, ICON_COLOR)
        value_surf = self.font_value.render(value, True, VALUE_COLOR)
        screen.blit(icon_surf, (x, y))
        screen.blit(value_surf, (x + icon_surf.get_width() + 8, y + 2))

    def draw_lives(self, screen: pygame.Surface) -> None:
        """Draws the player's remaining lives on the left side of the HUD.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        hud_center_y = int(self.state.offset_y // 2 - 15)
        start_x = 40
        spacing = 60

        for i in range(self.engine.lives):
            x = start_x + i * spacing
            if i < self.engine.player.lives:
                screen.blit(self.life_full, (x, hud_center_y))
            else:
                screen.blit(self.life_empty, (x, hud_center_y))

    def draw_right(self, screen: pygame.Surface) -> None:
        """Draws the right section of the HUD (score, level, remaining time).

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        elapsed = (
            time.time()
            - self.state.level_start
            - self.state.total_paused
        )
        remaining = max(0, self.engine.level_max_time - elapsed)

        hud_center_y = int(self.state.offset_y // 2 - 14)

        score_x = 980
        level_x = 1300
        time_x = 1620

        self._draw_item(
            screen, "★",
            str(self.engine.score),
            score_x, hud_center_y
        )
        level_str = (
            f"{self.engine.current_level}"
            f"/{len(self.engine.levels)}"
        )
        self._draw_item(
            screen, "◎", level_str,
            level_x, hud_center_y
        )

        time_color = TIME_WARN_COLOR if remaining <= 15 else VALUE_COLOR
        icon_surf = self.font_icon.render("◷", True, ICON_COLOR)
        value_surf = self.font_value.render(
            f"{int(remaining)}s", True, time_color
        )
        screen.blit(icon_surf, (time_x, hud_center_y))
        screen.blit(
            value_surf,
            (time_x + icon_surf.get_width() + 8,
             hud_center_y + 2)
        )
        self.life_empty.set_alpha(50)

    def render(self, screen: pygame.Surface) -> None:
        """Renders all components of the HUD.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        self.draw_right(screen)
        self.draw_lives(screen)


class PlayingState(GameState):
    """The main game state handling gameplay logic, updating, and rendering.

    Attributes:
        level_start (float): The timestamp when the current level started.
        total_paused (float): Total time spent in pause state.
        pause_start (float): The timestamp when the game was last paused.
        direction (str | None): The current movement direction of the player.
        next_direction (str | None): The buffered next movement direction.
        player_speed (float): The movement speed of the player per frame.
        engine (Engine): The main game engine handling game logic.
        mazegen (Any): The maze generator instance.
        screen (pygame.Surface): The main pygame display surface.
        hud (HUD): The Heads-Up Display instance.
        maze_width (int): Total width of the maze in pixels.
        maze_height (int): Total height of the maze in pixels.
        offset_x (float): Horizontal offset to center the maze.
        offset_y (float): Vertical offset to center the maze.
        maze_renderer (MazeRenderer): Renderer for the maze grid.
        pacgum_renderer (PacgumRenderer): Renderer for the pacgums.
        ghost_renderer (GhostRenderer): Renderer for the ghosts.
        player_renderer (PlayerRenderer): Renderer for the player.
        death_renderer (DeathAnimationRenderer): Renderer for death animation.
        dying (bool): Indicates if the death animation is currently playing.
    """
    def __init__(self, engine: Engine, screen: Any, fps: int = 30) -> None:
        """Initializes the PlayingState.

        Args:
            engine (Engine): The main game engine.
            screen (Any): The main pygame display surface.
            fps (int): Target frames per second. Defaults to 30.
        """
        self.level_start = time.time()
        self.total_paused: float = 0.0
        self.pause_start: float = 0.0

        self.direction: str | None = None
        self.next_direction: str | None = None
        self.player_speed = round(2 / fps, 1)

        self.engine = engine
        self.mazegen = self.engine.maze
        self.screen = screen

        self.hud = HUD(self.engine, self)

        assert self.mazegen is not None
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

        self.ghost_renderer = GhostRenderer(
            self.mazegen.ghosts,
            self.offset_x,
            self.offset_y
            )

        self.player_renderer = PlayerRenderer(
            self.engine.player,
            self.offset_x,
            self.offset_y
        )
        self.player_renderer._last_draw_x = 0
        self.player_renderer._last_draw_y = 0

        self.death_renderer = DeathAnimationRenderer()
        self.dying = False

    def update_renderers(self) -> None:
        """Updates all renderers based on the current maze and offsets.
        Typically called when transitioning to a new level.
        """
        self.mazegen = self.engine.maze
        assert self.mazegen is not None

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
        self.ghost_renderer = GhostRenderer(
            self.mazegen.ghosts,
            self.offset_x,
            self.offset_y
            )
        self.player_renderer.offset_x = self.offset_x
        self.player_renderer.offset_y = self.offset_y

    def update(self) -> Any:
        """Updates the game state logic, checking for win/loss conditions.

        Returns:
            Any: A tuple ('gameover', score) or ('victory', score)
                if the game ends, otherwise None.
        """
        if self.dying:
            return

        elapsed = time.time() - self.level_start - self.total_paused
        if elapsed > self.engine.level_max_time:
            return ('gameover', self.engine.score)

        if not self.engine.player.lives:
            return ('gameover', self.engine.score)

        self.move_player()
        result = self.engine.update()
        if result == 'death':
            self.dying = True
            self.direction = None
            self.next_direction = None
            x = self.player_renderer._last_draw_x
            y = self.player_renderer._last_draw_y
            self.death_renderer.start(x, y)
            return

        assert self.engine.maze is not None
        if self.engine.maze.pacgums_nb == 0:
            self.direction = None
            if not self.engine.start_next_level():
                return ('victory', self.engine.score)

            self.update_renderers()
            self.level_start = time.time()

    def handle_events(self, events: Any) -> Any:
        """Processes input events such as keyboard presses.

        Args:
            events (Any): An iterable of pygame events.

        Returns:
            Any: Returns a state string like 'quit' or 'pause' if requested,
                 otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            if self.dying:
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.direction = None
                    assert self.engine.maze is not None
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

    def render(self, screen: pygame.Surface) -> None:
        """Renders the entire playing state onto the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        screen.fill((22, 22, 30))

        self.maze_renderer.draw_maze(screen)
        self.pacgum_renderer.draw_pacgums(screen)
        self.ghost_renderer.draw_ghosts(screen)

        if self.dying:
            finished = self.death_renderer.update_and_draw(screen)
            if finished:
                self.dying = False
                self.engine.reset_after_death()
                self.death_renderer.reset()
        else:
            self.player_renderer.draw_player(screen, self.direction)

        self.hud.render(screen)

    def move_player(self) -> None:
        """Updates the player's position based on
        their current direction and speed.
        """
        x = self.engine.player.x
        y = self.engine.player.y
        assert self.engine.maze is not None
        maze = self.engine.maze.maze

        if self.engine.player.x % 1 == 0 and self.engine.player.y % 1 == 0:
            self.engine.player.x = int(self.engine.player.x)
            self.engine.player.y = int(self.engine.player.y)
        if (self.next_direction
                and self.can_move(
                    x, y, self.next_direction, maze)):
            self.direction = self.next_direction
            self.next_direction = None

        if self.direction and self.can_move(x, y, self.direction, maze):
            p = self.engine.player
            spd = self.player_speed
            if self.direction == "up":
                p.y = round(p.y - spd, 4)  # type: ignore[assignment]
            elif self.direction == "down":
                p.y = round(p.y + spd, 4)  # type: ignore[assignment]
            elif self.direction == "left":
                p.x = round(p.x - spd, 4)  # type: ignore[assignment]
            elif self.direction == "right":
                p.x = round(p.x + spd, 4)  # type: ignore[assignment]

    def can_move(
            self,
            x: float,
            y: float,
            direction: str,
            maze: list[list[int]]
            ) -> bool:
        """Determines if the player can move in the requested direction.

        Args:
            x (float): The current horizontal tile coordinate of the player.
            y (float): The current vertical tile coordinate of the player.
            direction (str): The direction to move
                    ('up', 'down', 'left', 'right').
            maze (list[list[int]]): The maze grid representing walls.

        Returns:
            bool: True if movement is allowed, False otherwise.
        """
        if not self.engine.ready:
            return False
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
