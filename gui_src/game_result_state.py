import pygame
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
    def __init__(self, score, highscore_filename, result, screen_width, screen_height):
        self.score = score
        self.highscore_filename = highscore_filename
        self.result = result
        self.cx = screen_width // 2
        self.cy = screen_height // 2 - 150
        self.font = pygame.font.Font("resources/PressStart2P-Regular.ttf", 36)
        self.font_input = pygame.font.Font("resources/PressStart2P-Regular.ttf", 14)
        self.user_txt = ''
        self.input_rect = pygame.Rect(self.cx - 100, self.cy + 40, 200, 40)
        self.gameovertext = self.font.render("Game Over", True, GAME_OVER_TEXT)
        self.victorytext = self.font.render("Victory", True, VICTORY_TEXT)
        self.score_text = self.font.render(f'You Get: {self.score}', True, SCORE_TEXT)
        self.color = COLOR_INACTIVE
        self.active =  False
        self.name_submitted = False
        button_w = 275
        button_h = 75
        gap = 25
        bx = screen_width // 2 - button_w // 2
        by = screen_height // 2 - 100
        self.rect_restart = pygame.Rect(bx, by, button_w, button_h)
        self.rect_menu    = pygame.Rect(bx, by + button_h + gap, button_w, button_h)
        self.rect_quit    = pygame.Rect(bx, by + (button_h + gap) * 2, button_w, button_h)
        self.bg = AnimatedBackground()

    def handle_events(self, events:pygame.event):
        for event in events:
            if event.type == pygame.QUIT :
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
                    self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.user_txt = self.user_txt[:-1]
                elif event.key == pygame.K_RETURN:
                    Engine.highscores_caching(self.user_txt, self.score, self.highscore_filename)
                    self.name_submitted = True
                    self.active = False
                else:
                    if len(self.user_txt) < 10 and (event.unicode.isalnum() or event.unicode.isspace()):
                        self.user_txt += event.unicode
    def update(self):
        self.bg.update(1 / 60)
    def render(self, screen: pygame.Surface):
        self.bg.render(screen)
        if self.result == 'gameover':
            screen.blit(self.gameovertext, (self.cx - self.gameovertext.get_width() // 2, self.cy - 120))
        elif self.result == 'victory':
            screen.blit(self.victorytext, (self.cx - self.victorytext.get_width() // 2, self.cy - 120))
        screen.blit(self.score_text, (self.cx - self.score_text.get_width() // 2, self.cy - 60))
        if not self.name_submitted:
            prompt = self.font_input.render("Enter your name (press Enter):", True, SCORE_TEXT)
            screen.blit(prompt, (self.cx - prompt.get_width() // 2, self.cy))
            text_surface = self.font_input.render(self.user_txt, True, COLOR_TEXT)
            self.input_rect.w = max(200, text_surface.get_width() + 10)
            screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 7))
            pygame.draw.rect(screen, self.color, self.input_rect, 2)
        else:
            saved = self.font_input.render(f"Score saved for {self.user_txt}! Try again and get a higher score!", True, SCORE_TEXT)
            screen.blit(saved, (self.cx - saved.get_width() // 2, self.cy))
            self.draw_button(screen, self.rect_restart, "Restart Game")
            self.draw_button(screen, self.rect_menu, "Menu")
            self.draw_button(screen, self.rect_quit, "Quit")

    def draw_button(self, screen: pygame.Surface, rect: pygame.Rect, label: str):
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        color      = HOVER_COLOR_BUTTON if hovered else OPTIONS_COLOR_BUTTON
        text_color = HOVER_COLOR_TEXT   if hovered else OPTIONS_COLOR_TEXT

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, OUTLINE_COLOR, rect, width=2, border_radius=8)
        text = self.font_input.render(label, True, text_color)
        screen.blit(text, text.get_rect(center=rect.center))
