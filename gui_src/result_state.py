import pygame
from typing import Any
from .game_state import GameState
from .background import AnimatedBackground
from engine import Engine
from webcolors import name_to_rgb, hex_to_rgb

GAME_OVER_TEXT = name_to_rgb('red')
VICTORY_TEXT = name_to_rgb('green')
SCORE_TEXT = name_to_rgb('white')
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('white')
OPTIONS_COLOR_BUTTON = name_to_rgb('gold')
HOVER_COLOR_BUTTON = hex_to_rgb('#1e1e1e')
OPTIONS_COLOR_TEXT = hex_to_rgb('#222222')
HOVER_COLOR_TEXT = name_to_rgb('gold')
OUTLINE_COLOR = name_to_rgb('gold')


class GameResultState(GameState):
    """Represents the game result state,
        handling both victory and game over scenarios.
    """

    def __init__(
        self, score: int, highscore_filename: str, result: str,
        screen_width: int, screen_height: int
    ) -> None:
        """Initializes the game result state.

        Args:
            score (int): The player's final score.
            highscore_filename (str): The filename used to save highscores.
            result (str): The result of the game ('victory' or 'gameover').
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.

        Returns:
            None
        """
        self.score = score
        self.highscore_filename = highscore_filename
        self.result = result
        self.cx = screen_width // 2
        self.cy = screen_height // 2 - 150
        self.font_result = pygame.font.Font(
            "resources/PressStart2P-Regular.ttf", 80
        )
        self.font_score = pygame.font.Font(
            "resources/PressStart2P-Regular.ttf", 45
        )
        self.font_btn = pygame.font.Font(
            "resources/PressStart2P-Regular.ttf", 19
        )
        self.font_input = pygame.font.Font(
            "resources/PressStart2P-Regular.ttf", 14
        )
        self.user_txt = ''
        self.input_rect = pygame.Rect(
            self.cx - 100, self.cy + 120, 200, 40
        )
        self.gameovertext = self.font_result.render(
            "Game Over", True, GAME_OVER_TEXT
        )
        self.victorytext = self.font_result.render(
            "Victory", True, VICTORY_TEXT
        )
        self.score_text = self.font_score.render(
            f'You Get: {self.score}', True, SCORE_TEXT
        )
        self.color = COLOR_INACTIVE
        self.active = False
        self.name_submitted = False
        button_w = 275
        button_h = 75
        gap = 25
        bx = screen_width // 2 - button_w // 2
        by = screen_height // 2
        self.rect_restart = pygame.Rect(bx, by, button_w, button_h)
        self.rect_menu = pygame.Rect(
            bx, by + button_h + gap, button_w, button_h
        )
        self.rect_quit = pygame.Rect(
            bx, by + (button_h + gap) * 2,
            button_w, button_h
        )
        self.bg = AnimatedBackground()

    def handle_events(self, events: Any) -> Any:
        """Handles user input events for the result screen.

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
                if self.name_submitted:
                    if self.rect_restart.collidepoint(event.pos):
                        return 'restart'
                    elif self.rect_menu.collidepoint(event.pos):
                        return 'main'
                    elif self.rect_quit.collidepoint(event.pos):
                        return 'quit'
                else:
                    if self.input_rect.collidepoint(event.pos):
                        self.active = True
                    else:
                        self.active = False
                    self.color = (
                        COLOR_ACTIVE if self.active
                        else COLOR_INACTIVE
                    )

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.user_txt = self.user_txt[:-1]
                elif event.key == pygame.K_RETURN:
                    Engine.highscores_caching(
                        self.user_txt, self.score,
                        self.highscore_filename
                    )
                    self.name_submitted = True
                    self.active = False
                else:
                    if (
                        len(self.user_txt) < 10
                        and (event.unicode.isalnum()
                             or event.unicode.isspace())
                    ):
                        self.user_txt += event.unicode

    def update(self) -> Any:
        """Updates the game result state.

        Returns:
            Any: None.
        """
        self.bg.update(1 / 60)

    def render(self, screen: pygame.Surface) -> None:
        """Renders the result screen to the surface.

        Args:
            screen (pygame.Surface): The surface to
                render the result screen on.

        Returns:
            None
        """
        self.bg.render(screen)
        if self.result == 'gameover':
            go_x = self.cx - self.gameovertext.get_width() // 2
            screen.blit(
                self.gameovertext, (go_x, self.cy - 120)
            )
        elif self.result == 'victory':
            v_x = self.cx - self.victorytext.get_width() // 2
            screen.blit(
                self.victorytext, (v_x, self.cy - 120)
            )
        s_x = self.cx - self.score_text.get_width() // 2
        screen.blit(self.score_text, (s_x, self.cy))
        if not self.name_submitted:
            prompt = self.font_input.render(
                "Enter your name to save your "
                "score (press Enter):",
                True, SCORE_TEXT
            )
            p_x = self.cx - prompt.get_width() // 2
            screen.blit(prompt, (p_x, self.cy + 80))
            text_surface = self.font_input.render(
                self.user_txt, True, COLOR_TEXT
            )
            self.input_rect.w = max(
                200, text_surface.get_width() + 10
            )
            screen.blit(text_surface, (
                self.input_rect.x + 5,
                self.input_rect.y + 7
            ))
            pygame.draw.rect(screen, self.color, self.input_rect, 2)
        else:
            saved = self.font_input.render(
                f"Score saved for {self.user_txt}!"
                " Try again and get a higher score!",
                True, SCORE_TEXT
            )
            sv_x = self.cx - saved.get_width() // 2
            screen.blit(saved, (sv_x, self.cy + 80))
            self.draw_button(screen, self.rect_restart, "Restart Game")
            self.draw_button(screen, self.rect_menu, "Menu")
            self.draw_button(screen, self.rect_quit, "Quit")

    def draw_button(
        self, screen: pygame.Surface,
        rect: pygame.Rect, label: str
    ) -> None:
        """Draws a button on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the button on.
            rect (pygame.Rect): The rectangular area of the button.
            label (str): The text label to display on the button.

        Returns:
            None
        """
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        color = HOVER_COLOR_BUTTON if hovered else OPTIONS_COLOR_BUTTON
        text_color = HOVER_COLOR_TEXT if hovered else OPTIONS_COLOR_TEXT

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(
            screen, OUTLINE_COLOR, rect,
            width=2, border_radius=8
        )
        text = self.font_btn.render(label, True, text_color)
        screen.blit(text, text.get_rect(center=rect.center))
