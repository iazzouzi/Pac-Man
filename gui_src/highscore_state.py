import pygame

from .background import AnimatedBackground
from .game_state import GameState
from webcolors import name_to_rgb, hex_to_rgb

SCORE_BG_COLOR = name_to_rgb('gold')
NAME_COLOR = hex_to_rgb('#222222')
SCORE_COLOR = name_to_rgb('gray')
ARROW_COLOR = name_to_rgb('white')
ARROW_HOVER_COLOR = name_to_rgb('yellow')

class HighscoreState(GameState):
    def __init__(self, screen_width, screen_height, top_scores: dict[str, int]):
        self.top_scores = top_scores
        self.screen_width = screen_width
        self.screen_height = screen_height
        score_w = 1300
        score_h = 130
        gap = 25
        sx = screen_width // 2 - score_w // 2
        sy = screen_height // 2 - 350
        self.scores_rect = {
            i: pygame.Rect(sx, sy + (score_h + gap) * i, score_w, score_h)
            for i in range(len(top_scores.items()))
        }
        self.arrow_rect = pygame.Rect(50, 50, 70, 70)
        self.font_scores = pygame.font.Font(None, 40)
        self.font_title = pygame.font.Font(None, 70)
        self.font_arrow = pygame.font.SysFont("dejavusans", 90)
        self.bg = AnimatedBackground()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.arrow_rect.collidepoint(event.pos):
                    return 'main'
    def update(self):
        self.bg.update(1 / 60)
    def render(self, screen: pygame.Surface):
        self.bg.render(screen)
        title = self.font_title.render("Highscores", True, SCORE_BG_COLOR)
        hovered = self.arrow_rect.collidepoint(pygame.mouse.get_pos())
        arrow_color = ARROW_HOVER_COLOR if hovered else ARROW_COLOR
        arrow = self.font_arrow.render("←", True, arrow_color)
        screen.blit(title, title.get_rect(midtop=(self.screen_width // 2, 75)))
        screen.blit(arrow, arrow.get_rect(topleft=(50, 50)))
        for rect, scores in zip(self.scores_rect.items(), self.top_scores.items()):
            pygame.draw.rect(screen, SCORE_BG_COLOR, rect[1], border_radius=8)
            name = self.font_scores.render(scores[0], True, NAME_COLOR)
            score = self.font_scores.render(str(scores[1]), True, SCORE_COLOR)
            screen.blit(score, score.get_rect(center = rect[1].center))
            screen.blit(name, name.get_rect(midleft=(rect[1].left + 160, rect[1].centery)))
            if rect[0] == 0 :
                pygame.draw.circle(screen, name_to_rgb('purple'), (rect[1].right - 270, rect[1].centery), 30)
            elif rect[0] == 1 :
                pygame.draw.circle(screen, name_to_rgb('silver'), (rect[1].right - 270, rect[1].centery), 30)
            elif rect[0] == 2 :
                pygame.draw.circle(screen, name_to_rgb('lightblue'), (rect[1].right - 270, rect[1].centery), 30)
            else :
                pygame.draw.circle(screen, name_to_rgb('crimson'), (rect[1].right - 270, rect[1].centery), 30)
