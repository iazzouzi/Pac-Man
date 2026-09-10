import pygame, math
from .game_state import GameState

GRID_SPACING = 40
GRID_SPEED = 60
PULSE_SPEED = 1.5

class AnimatedBackground(GameState):
    def __init__(self):
        self.offset = 0.0
        self.pulse = 0.0

    def update(self, dt):
        self.offset = (self.offset + GRID_SPEED * dt) % GRID_SPACING
        self.pulse += PULSE_SPEED * dt

    def render(self, surface: pygame.Surface):
        surface.fill((22, 22, 30))
        
        alpha = int(25 + 10 * math.sin(self.pulse))
        grid_color = (80, 120, 220, alpha)
        
        grid_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        
        for x in range(-GRID_SPACING + int(self.offset), surface.get_width() + GRID_SPACING, GRID_SPACING):
            pygame.draw.line(grid_surf, grid_color, (x, 0), (x, surface.get_height()))
        
        for y in range(-GRID_SPACING + int(self.offset), surface.get_height() + GRID_SPACING, GRID_SPACING):
            pygame.draw.line(grid_surf, grid_color, (0, y), (surface.get_width(), y))
        
        surface.blit(grid_surf, (0, 0))