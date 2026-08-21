import pygame
from game_state import GameState
from webcolors import name_to_rgb, hex_to_rgb

OPTIONS_COLOR_TEXT = hex_to_rgb('#222222')
OPTIONS_COLOR_BUTTON = name_to_rgb('gold')
HOVER_COLOR_BUTTON = hex_to_rgb('#1e1e1e')
HOVER_COLOR_TEXT = name_to_rgb('gold')
OUTLINE_COLOR = name_to_rgb('gold')


class MainMenuState(GameState):
    def __init__(self, screen_width: int, screen_height: int):
        self.font = pygame.font.Font(None, 38)
        self.font_title = pygame.font.Font(None, 100)

        button_w = 275
        button_h = 75
        gap = 25
        x = screen_width // 2 - button_w // 2
        start_y = screen_height // 2 - 100

        self.rect_start = pygame.Rect(x, start_y, button_w, button_h)
        self.rect_high  = pygame.Rect(x, start_y + (button_h + gap), button_w, button_h)
        self.rect_inst  = pygame.Rect(x, start_y + (button_h + gap) * 2, button_w, button_h)
        self.rect_exit  = pygame.Rect(x, start_y + (button_h + gap) * 3, button_w, button_h)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT :
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect_start.collidepoint(event.pos):
                    return 'playing'
                elif self.rect_exit.collidepoint(event.pos):
                    return 'quit'

    def render(self, screen):
        screen.fill((30,30,30))
        self.draw_title(screen)
        self.draw_start(screen)
        self.draw_highscore(screen)
        self.draw_instructions(screen)
        self.draw_exit(screen)
        pygame.display.flip()

    def draw_button(self, screen: pygame.Surface, rect: pygame.Rect, label: str):
        mouse = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse)
        color = HOVER_COLOR_BUTTON if hovered else OPTIONS_COLOR_BUTTON
        text_color = HOVER_COLOR_TEXT if hovered else OPTIONS_COLOR_TEXT

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, OUTLINE_COLOR, rect, width=2, border_radius=8)

        text = self.font.render(label, True, text_color)
        screen.blit(text, text.get_rect(center=rect.center))
    
    def draw_title(self, screen: pygame.surface):
        text = self.font_title.render("PAC-MAN", True, OPTIONS_COLOR_BUTTON)
        screen.blit(text, (790, 190))

    def draw_start(self, screen):
        self.draw_button(screen, self.rect_start, "Start Game")

    def draw_highscore(self, screen):
        self.draw_button(screen, self.rect_high, "Highscore")

    def draw_instructions(self, screen):
        self.draw_button(screen, self.rect_inst, "Instructions")

    def draw_exit(self, screen):
        self.draw_button(screen, self.rect_exit, "Exit")