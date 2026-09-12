import pygame
from typing import Any
from .game_state import GameState
from .background import AnimatedBackground
from engine import Engine
from webcolors import name_to_rgb, hex_to_rgb

OPTIONS_COLOR_TEXT = hex_to_rgb('#222222')
OPTIONS_COLOR_BUTTON = name_to_rgb('gold')
HOVER_COLOR_BUTTON = hex_to_rgb('#1e1e1e')
HOVER_COLOR_TEXT = name_to_rgb('gold')
OUTLINE_COLOR = name_to_rgb('gold')


class MainMenuState(GameState):
    """Represents the main menu state of the game."""

    def __init__(self, screen_width: int, screen_height: int):
        """Initializes the main menu state.

        Args:
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
        """
        self.font = pygame.font.Font(
            Engine.get_asset_path("resources/PressStart2P-Regular.ttf"), 19
        )
        self.font_title = pygame.font.Font(
            Engine.get_asset_path("resources/PressStart2P-Regular.ttf"), 70
        )

        self.bg = AnimatedBackground()

        button_w = 370
        button_h = 75
        gap = 25
        x = screen_width // 2 - button_w // 2
        start_y = screen_height // 2 - 100

        self.rect_start = pygame.Rect(x, start_y, button_w, button_h)
        self.rect_high = pygame.Rect(
            x, start_y + (button_h + gap),
            button_w, button_h
        )
        self.rect_inst = pygame.Rect(
            x, start_y + (button_h + gap) * 2,
            button_w, button_h
        )
        self.rect_exit = pygame.Rect(
            x, start_y + (button_h + gap) * 3,
            button_w, button_h
        )

    def handle_events(self, events: Any) -> Any:
        """Handles user input events for the main menu.

        Args:
            events (Any): A list of pygame events to process.

        Returns:
            Any: A string indicating the next state,
                or None if no state change is needed.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect_start.collidepoint(event.pos):
                    return 'playing'
                elif self.rect_high.collidepoint(event.pos):
                    return 'highscores'
                elif self.rect_inst.collidepoint(event.pos):
                    return 'instructions'
                elif self.rect_exit.collidepoint(event.pos):
                    return 'quit'

    def update(self) -> Any:
        """Updates the main menu state.

        Returns:
            Any: None.
        """
        self.bg.update(1 / 60)

    def render(self, screen: pygame.Surface) -> None:
        """Renders the main menu to the screen.

        Args:
            screen (pygame.Surface): The surface to render the menu on.

        Returns:
            None
        """
        self.bg.render(screen)
        self.draw_title(screen)
        self.draw_start(screen)
        self.draw_highscore(screen)
        self.draw_instructions(screen)
        self.draw_exit(screen)

    def draw_button(
        self, screen: pygame.Surface, rect: pygame.Rect, label: str
    ) -> None:
        """Draws a button on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the button on.
            rect (pygame.Rect): The rectangular area of the button.
            label (str): The text label to display on the button.

        Returns:
            None
        """
        mouse = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse)
        color = HOVER_COLOR_BUTTON if hovered else OPTIONS_COLOR_BUTTON
        text_color = HOVER_COLOR_TEXT if hovered else OPTIONS_COLOR_TEXT

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, OUTLINE_COLOR, rect, width=2, border_radius=8)

        text = self.font.render(label, True, text_color)
        screen.blit(text, text.get_rect(center=rect.center))

    def draw_title(self, screen: pygame.Surface) -> None:
        """Draws the game title on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the title on.

        Returns:
            None
        """
        text = self.font_title.render("PAC-MAN", True, OPTIONS_COLOR_BUTTON)
        text_rect = text.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 4)
        )
        screen.blit(text, text_rect)

    def draw_start(self, screen: pygame.Surface) -> None:
        """Draws the start game button on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the button on.

        Returns:
            None
        """
        self.draw_button(screen, self.rect_start, "Start Game")

    def draw_highscore(self, screen: pygame.Surface) -> None:
        """Draws the view highscores button on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the button on.

        Returns:
            None
        """
        self.draw_button(screen, self.rect_high, "View Highscores")

    def draw_instructions(self, screen: pygame.Surface) -> None:
        """Draws the instructions button on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the button on.

        Returns:
            None
        """
        self.draw_button(screen, self.rect_inst, "Instructions")

    def draw_exit(self, screen: pygame.Surface) -> None:
        """Draws the exit button on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the button on.

        Returns:
            None
        """
        self.draw_button(screen, self.rect_exit, "Exit")
