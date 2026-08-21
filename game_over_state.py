import pygame
from game_state import GameState
from engine import Engine
from webcolors import name_to_rgb

GAME_OVER_TEXT = name_to_rgb('red')
SCORE_TEXT = name_to_rgb('white')
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('white')

class GameOverState(GameState):
    def __init__(self, score, highscore_filename):
        self.score = score
        self.highscore_filename = highscore_filename
        self.font = pygame.font.Font(None, 80)
        self.font_input = pygame.font.Font(None, 32)
        self.user_txt = ''
        self.input_rect = pygame.Rect(170, 170, 200, 40)
        self.color = COLOR_INACTIVE
        self.active =  False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT :
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.user_txt = self.user_txt[:-1]
                elif event.key == pygame.K_RETURN:
                    Engine.highscores_caching(self.user_txt, self.score, self.highscore_filename)
                    return 'main'
                else:
                    self.user_txt += event.unicode

    def render(self, screen: pygame.surface):
        screen.fill((30, 30, 30))
        self.gameovertext = self.font.render("Game Over", True, GAME_OVER_TEXT)
        self.score_text = self.font.render(f'You Get: {self.score}', True, SCORE_TEXT)
        screen.blit(self.gameovertext, (20, 50))
        screen.blit(self.score_text, (20, 100))


        self.text_surface = self.font_input.render(self.user_txt, True, COLOR_TEXT)
        self.input_rect.w = max(200, self.text_surface.get_width() + 10)
        screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 7))

        pygame.draw.rect(screen, self.color, self.input_rect, 2)
