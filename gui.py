from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from engine import Engine
from game_over_state import GameOverState
from main_menu_state import MainMenuState
from playing_state import PlayingState

class Game:
    def __init__(self, engine: Engine):
        pygame.init()

        self.screen = pygame.display.set_mode((1920, 1080))
        self.fps = pygame.time.Clock()
        pygame.display.set_caption("Pacman")

        self.running = True
        self.engine = engine

        self.current_state = MainMenuState(self.screen.get_width(), self.screen.get_height())

    def run(self):
        while self.running:
            events = pygame.event.get()

            result = self.current_state.handle_events(events)
            self.change_state(result)

            if not self.running:
                break

            result = self.current_state.update()
            self.change_state(result)

            self.current_state.render(self.screen)
            pygame.display.flip()
            self.fps.tick(5.5) 

    def change_state(self, result):
        if result == 'playing':
            self.current_state = PlayingState(
                self.engine,
                self.screen
            )
        if isinstance(result, tuple) and result[0] == 'gameover':
            self.current_state = GameOverState(
                result[1],
                self.engine.highscore_filename
            )
            return
        if result == 'main':
            self.current_state = MainMenuState(self.screen.get_width(), self.screen.get_height())
        if result == 'quit':
            self.running = False
            pygame.quit()
            return