import pygame
from typing import Any
from .background import AnimatedBackground
from .game_state import GameState
from webcolors import name_to_rgb, hex_to_rgb

BOX_BG_COLOR = (20, 20, 40)
BOX_BORDER = name_to_rgb('gold')
NAME_COLOR = hex_to_rgb("#FFFFFF")
SCORE_COLOR = hex_to_rgb("#FFFFFF")
TITLE_COLOR = name_to_rgb('gold')
ARROW_COLOR = name_to_rgb('white')
ARROW_HOVER_COLOR = name_to_rgb('yellow')


class HighscoreState(GameState):
    """Represents the highscore screen of the game.

    This state displays the top scores achieved by players, including their ranks and icons.
    """
    def __init__(
        self, screen_width: int, screen_height: int,
        top_scores: dict[str, int]
    ) -> None:
        """Initializes the HighscoreState.

        Args:
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
            top_scores (dict[str, int]): A dictionary mapping player names to their top scores.
        """
        self.top_scores = top_scores
        self.screen_width = screen_width
        self.screen_height = screen_height
        score_w = 1150
        score_h = 75
        gap = 12
        sx = screen_width // 2 - score_w // 2
        sy = screen_height // 2 - 435
        self.scores_rect = {
            i: pygame.Rect(sx, sy + (score_h + gap) * i, score_w, score_h)
            for i in range(len(top_scores.items()))
        }
        self.arrow_rect = pygame.Rect(50, 50, 70, 70)
        self.font_scores = pygame.font.Font(
            "resources/PressStart2P-Regular.ttf", 18
        )
        self.font_empty = pygame.font.Font(
            "resources/PressStart2P-Regular.ttf", 80
        )
        self.font_title = pygame.font.Font(
            "resources/PressStart2P-Regular.ttf", 32
        )
        self.font_arrow = pygame.font.SysFont(
            "dejavusans", 90
        )
        self.font_rank = pygame.font.Font(
            "resources/PressStart2P-Regular.ttf", 16
        )
        self.crown = pygame.transform.smoothscale(
            pygame.image.load(
                "assets/crown.png"
            ).convert_alpha(), (80, 80)
        )
        self.trophy = pygame.transform.smoothscale(
            pygame.image.load(
                "assets/trophy.png"
            ).convert_alpha(), (60, 60)
        )
        self.medal = pygame.transform.smoothscale(
            pygame.image.load(
                "assets/medal.png"
            ).convert_alpha(), (80, 60)
        )
        self.bg = AnimatedBackground()

    def handle_events(self, events: Any) -> Any:
        """Handles user input events for the highscore state.

        Args:
            events (Any): A list of pygame events to process.

        Returns:
            Any: A string indicating the next state ('quit' or 'main'), or None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.arrow_rect.collidepoint(event.pos):
                    return 'main'

    def update(self) -> Any:
        """Updates the highscore state logic.

        Returns:
            Any: None.
        """
        self.bg.update(1 / 60)

    def render(self, screen: pygame.Surface) -> None:
        """Renders the highscore screen to the display.

        Args:
            screen (pygame.Surface): The main display surface to draw on.
        """
        self.bg.render(screen)
        title = self.font_title.render("Highscores", True, TITLE_COLOR)
        hovered = self.arrow_rect.collidepoint(pygame.mouse.get_pos())
        arrow_color = ARROW_HOVER_COLOR if hovered else ARROW_COLOR
        arrow = self.font_arrow.render("←", True, arrow_color)
        screen.blit(
            title,
            title.get_rect(
                midtop=(self.screen_width // 2, 40)
            )
        )
        screen.blit(arrow, arrow.get_rect(topleft=(50, 50)))
        if not self.top_scores:
            no_scores = self.font_empty.render(
                "No scores yet!", True, NAME_COLOR
            )
            screen.blit(
                no_scores,
                no_scores.get_rect(
                    center=(
                        self.screen_width // 2,
                        self.screen_height // 2
                    )
                )
            )
            return
        for rect, scores in zip(
            self.scores_rect.items(),
            self.top_scores.items()
        ):
            pygame.draw.rect(screen, BOX_BG_COLOR, rect[1], border_radius=8)
            pygame.draw.rect(
                screen, BOX_BORDER, rect[1],
                width=2, border_radius=10
            )
            name = self.font_scores.render(scores[0], True, NAME_COLOR)
            score = self.font_scores.render(str(scores[1]), True, SCORE_COLOR)
            screen.blit(
                score,
                score.get_rect(
                    midright=(
                        rect[1].right - 160,
                        rect[1].centery
                    )
                )
            )
            screen.blit(name, name.get_rect(center=rect[1].center))
            icon_x = rect[1].left + 100
            icon_y = rect[1].centery
            if rect[0] == 0:
                screen.blit(
                    self.crown,
                    self.crown.get_rect(
                        center=(icon_x, icon_y)
                    )
                )
            elif rect[0] == 1:
                screen.blit(
                    self.trophy,
                    self.trophy.get_rect(
                        center=(icon_x, icon_y)
                    )
                )
            elif rect[0] == 2:
                screen.blit(
                    self.medal,
                    self.medal.get_rect(
                        center=(icon_x, icon_y)
                    )
                )
            else:
                pygame.draw.circle(
                    screen, name_to_rgb('silver'),
                    (icon_x, icon_y), 30, 3
                )
                rank_text = self.font_rank.render(
                    str(rect[0] + 1), True,
                    name_to_rgb('silver')
                )
                screen.blit(
                    rank_text,
                    rank_text.get_rect(
                        center=(icon_x, icon_y)
                    )
                )
