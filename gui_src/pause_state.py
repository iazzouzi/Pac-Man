import pygame
from webcolors import name_to_rgb, hex_to_rgb
from .game_state import GameState


class PauseState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'resume'
    def render(self, screen:pygame.Surface):
        font = pygame.font.Font(None, 150)
        text = font.render("PAUSED", True, name_to_rgb('gold'))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(text, text_rect)