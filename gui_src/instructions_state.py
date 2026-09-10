import pygame

from engine import Engine
from .game_state import GameState
from webcolors import name_to_rgb

ARROW_COLOR = name_to_rgb('white')
ARROW_HOVER_COLOR = name_to_rgb('yellow')
TITLE_COLOR = name_to_rgb('gold')
SECTION_COLOR = name_to_rgb('yellow')
TEXT_COLOR = name_to_rgb('white')
BOX_BG = (20, 20, 40)
BOX_BORDER = name_to_rgb('gold')

class InstructionsState(GameState):
    def __init__(self, screen_width, screen_height, engine: Engine):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.arrow_rect = pygame.Rect(50, 50, 70, 70)
        self.font_arrow = pygame.font.SysFont("dejavusans", 90)
        self.font_title = pygame.font.Font(None, 70)
        self.font_section = pygame.font.Font(None, 34)
        self.font_body = pygame.font.Font(None, 40)

        p = engine.points_per_pacgum
        sp = engine.points_per_super_pacgum
        gp = engine.points_per_ghost
        lives = engine.lives
        t = int(engine.level_max_time)

        self.instructions: list[tuple[str, list[str]]] = [
            ("Objective & Scoring", [
                "Clear all PacGums in the maze to complete the level and advance.",
                f"Eating a PacGum earns {p} points.",
                f"Eating a Super PacGum earns {sp} points and makes ghosts vulnerable.",
                f"Eating an edible ghost earns {gp} points.",
                f"You start with {lives} lives. Survive all 10 levels to win.",
                f"Each level has a {t}s time limit — keep an eye on the timer!",
            ]),
            ("Super PacGums & Ghosts", [
                "Four Super PacGums sit in the corners of the maze.",
                "Eating one turns all ghosts blue and edible for 10 seconds.",
                f"Move into a blue ghost to eat it for {gp} points.",
                "Touching a normal ghost costs a life and resets all positions.",
                "Blinky (Red) chases you directly.",
                "Pinky (Pink) ambushes 2 cells ahead of your direction.",
                "Inky (Cyan) uses Blinky's position to flank you.",
                "Clyde (Orange) targets 2 cells behind you.",
            ]),
            ("Controls", [
                "Arrow Keys or WASD — move Pac-Man in four directions.",
                "Escape — pause the game.",
                "Your input is buffered: Pac-Man turns as soon as the path clears.",
            ]),
            ("Cheat Mode", [
                "0 — toggle Invincibility (ghosts cannot kill you).",
                "1 — toggle Ghost Freeze (ghosts stop moving).",
                "Space — skip the current level instantly.",
            ]),
        ]

        pad = 60
        box_w = screen_width - pad * 2 - 450
        self.box_rect = pygame.Rect(
            (screen_width - box_w) // 2, 160,
            box_w,
            screen_height - 160 - pad - 50,
        )

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

    def render(self, screen):
        screen.fill((30, 30, 30))

        title = self.font_title.render("Instructions", True, TITLE_COLOR)
        screen.blit(title, title.get_rect(midtop=(self.screen_width // 2, 75)))

        hovered = self.arrow_rect.collidepoint(pygame.mouse.get_pos())
        arrow = self.font_arrow.render("←", True, ARROW_HOVER_COLOR if hovered else ARROW_COLOR)
        screen.blit(arrow, arrow.get_rect(topleft=(50, 50)))

        pygame.draw.rect(screen, BOX_BG, self.box_rect, border_radius=10)
        pygame.draw.rect(screen, BOX_BORDER, self.box_rect, width=2, border_radius=10)

        x = self.box_rect.x + 20
        y = self.box_rect.y + 23

        for section_title, bullets in self.instructions:
            surf = self.font_section.render(section_title, True, SECTION_COLOR)
            screen.blit(surf, (x, y))
            y += self.font_section.get_linesize() + 8

            for bullet in bullets:
                surf = self.font_body.render(bullet, True, TEXT_COLOR)
                screen.blit(surf, (x + 18, y))
                y += self.font_body.get_linesize()

            y += 12