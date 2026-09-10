import pygame
from webcolors import name_to_rgb, hex_to_rgb

from .background import AnimatedBackground
from .game_state import GameState

OPTIONS_COLOR_BUTTON = name_to_rgb('gold')
HOVER_COLOR_BUTTON = hex_to_rgb('#1e1e1e')
OPTIONS_COLOR_TEXT = hex_to_rgb('#222222')
HOVER_COLOR_TEXT = name_to_rgb('gold')
OUTLINE_COLOR = name_to_rgb('gold')

class PauseState(GameState):
    def __init__(self, screen_width, screen_height):
        self.font_button = pygame.font.Font("resources/PressStart2P-Regular.ttf", 19)
        self.font_title = pygame.font.Font("resources/PressStart2P-Regular.ttf", 70)
        button_w = 370
        button_h = 75
        gap = 25
        bx = screen_width // 2 - button_w // 2
        by = screen_height // 2 - 130
        self.rect_resume = pygame.Rect(bx, by, button_w, button_h)
        self.rect_restart    = pygame.Rect(bx, by + button_h + gap, button_w, button_h)
        self.rect_menu    = pygame.Rect(bx, by + (button_h + gap) * 2, button_w, button_h)
        self.bg = AnimatedBackground()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'resume'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect_resume.collidepoint(event.pos):
                    return 'resume'
                elif self.rect_restart.collidepoint(event.pos):
                    return 'restart'
                elif self.rect_menu.collidepoint(event.pos):
                    return 'main'
    def update(self):
        self.bg.update(1 / 60)
    def render(self, screen:pygame.Surface):
        self.bg.render(screen)
        text = self.font_title.render("PAUSED", True, name_to_rgb('gold'))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(text, text_rect)
        self.draw_button(screen, self.rect_resume, "Resume")
        self.draw_button(screen, self.rect_restart, "Restart Game")
        self.draw_button(screen, self.rect_menu, "Exit To Menu")

    def draw_button(self, screen: pygame.Surface, rect: pygame.Rect, label: str):
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        color      = HOVER_COLOR_BUTTON if hovered else OPTIONS_COLOR_BUTTON
        text_color = HOVER_COLOR_TEXT   if hovered else OPTIONS_COLOR_TEXT

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, OUTLINE_COLOR, rect, width=2, border_radius=8)
        text = self.font_button.render(label, True, text_color)
        screen.blit(text, text.get_rect(center=rect.center))