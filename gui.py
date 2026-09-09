from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame, time
from engine import Engine
from states import GameOverState, MainMenuState, PlayingState, PauseState

class Game:
    def __init__(self, engine: Engine):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((1920, 1080))
        self.fps = pygame.time.Clock()
        pygame.display.set_caption("PAC-MAN")

        self.running = True
        self.engine = engine
        self.engine.pacgum_sound = pygame.mixer.Sound("resources/eating_pacgum.mp3")
        self.engine.fail_sound = pygame.mixer.Sound("resources/fail.mp3")
        self.engine.eating_ghost_sound = pygame.mixer.Sound("resources/eating_ghost.mp3")
        self.engine.return_sound = pygame.mixer.Sound("resources/return.mp3")
        self.engine.edible_ghosts_sound = pygame.mixer.Sound("resources/edible_ghosts.mp3")
        self.engine.ghosts_move_sound = pygame.mixer.Sound("resources/ghosts_move.mp3")

        self.current_state = MainMenuState(self.screen.get_width(), self.screen.get_height())
        self.playing_state = None

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
            self.fps.tick(10)

    def change_state(self, result):
        if result == 'playing':
            self.playing_state = PlayingState(self.engine, self.screen)
            self.current_state = self.playing_state
        elif result == 'pause':
            self.playing_state.pause_start = time.time()
            self.current_state = PauseState()

        elif result == 'resume':
            self.playing_state.total_paused += time.time() - self.playing_state.pause_start
            self.current_state = self.playing_state
        elif isinstance(result, tuple) and result[0] == 'gameover':
            self.current_state = GameOverState(
                result[1],
                self.engine.highscore_filename
            )
            return
        elif result == 'main':
            self.current_state = MainMenuState(self.screen.get_width(), self.screen.get_height())
        elif result == 'quit':
            self.running = False
            pygame.quit()
            return