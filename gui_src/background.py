import pygame


GRID_SPACING = 40
GRID_SPEED = 60
GRID_ALPHA = 25


class AnimatedBackground:
    def __init__(self) -> None:
        self.offset = 0.0

    def update(self, dt: float) -> None:
        self.offset = (self.offset + GRID_SPEED * dt) % GRID_SPACING

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((22, 22, 30))

        grid_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        grid_color = (80, 120, 220, GRID_ALPHA)

        for x in range(
            -GRID_SPACING + int(self.offset),
            surface.get_width() + GRID_SPACING,
            GRID_SPACING,
        ):
            pygame.draw.line(
                grid_surf, grid_color,
                (x, 0), (x, surface.get_height()),
            )

        for y in range(
            -GRID_SPACING + int(self.offset),
            surface.get_height() + GRID_SPACING,
            GRID_SPACING,
        ):
            pygame.draw.line(
                grid_surf, grid_color,
                (0, y), (surface.get_width(), y),
            )

        surface.blit(grid_surf, (0, 0))
