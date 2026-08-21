from pickle import NONE

import pygame
from game_state import GameState
from webcolors import name_to_rgb, hex_to_rgb

OPTIONS_COLOR_TEXT = hex_to_rgb('#222222')
OPTIONS_COLOR_BUTTON = name_to_rgb('gold')
HOVER_COLOR = name_to_rgb('blue')


class MainMenuState(GameState):
    def __init__(self):
        self.font = pygame.font.Font(None, 38)
        self.font_title = pygame.font.Font(None, 100)
        self.rect_start = pygame.Rect(823, 425, 275, 75)
        self.rect_high= pygame.Rect(823, 525, 275, 75)
        self.rect_inst = pygame.Rect(823, 625, 275, 75)
        self.rect_exit = pygame.Rect(823, 725, 275, 75)
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

    def draw_title(self, screen: pygame.surface):
        text = self.font_title.render("PAC-MAN", True, OPTIONS_COLOR_BUTTON)
        screen.blit(text, (790, 190))

    def draw_start(self, screen:pygame.surface):
        button = pygame.draw.rect(screen, OPTIONS_COLOR_BUTTON, self.rect_start)
        text = self.font.render("Start Game", True, OPTIONS_COLOR_TEXT)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)

    def draw_highscore(self, screen:pygame.surface):
        button = pygame.draw.rect(screen, OPTIONS_COLOR_BUTTON, self.rect_high)
        text = self.font.render("Highscore", True, OPTIONS_COLOR_TEXT)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)

    def draw_instructions(self, screen:pygame.surface):
        button = pygame.draw.rect(screen, OPTIONS_COLOR_BUTTON, self.rect_inst)
        text = self.font.render("Instructions", True, OPTIONS_COLOR_TEXT)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)

    def draw_exit(self, screen:pygame.surface):
        button = pygame.draw.rect(screen, OPTIONS_COLOR_BUTTON, self.rect_exit)
        text = self.font.render("Exit", True, OPTIONS_COLOR_TEXT)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)
