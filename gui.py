from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame, time
from engine import Engine
from gui_src import *

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

    def reset_engine(self):
        self.engine.score = 0
        self.engine.current_level = 0
        self.engine.player.lives = self.engine.lives
        self.engine.start_next_level()

    def change_state(self, result):
        if result == 'playing':
            self.reset_engine()
            self.playing_state = PlayingState(self.engine, self.screen)
            self.current_state = self.playing_state
        elif result == 'restart':
            self.reset_engine()
            self.playing_state = PlayingState(self.engine, self.screen)
            self.current_state = self.playing_state

        elif result == 'pause':
            pygame.mixer.pause()
            self.playing_state.pause_start = time.time()
            self.current_state = PauseState(self.screen.get_width(), self.screen.get_height())

        elif result == 'resume':
            pygame.mixer.unpause()
            self.playing_state.total_paused += time.time() - self.playing_state.pause_start
            self.current_state = self.playing_state

        elif isinstance(result, tuple):
            pygame.mixer.stop()
            self.current_state = GameResultState(
                result[1],
                self.engine.highscore_filename, result[0], self.screen.get_width(),
                self.screen.get_height()
            )
            return
        elif result == 'main':
            self.current_state = MainMenuState(
                self.screen.get_width(),
                self.screen.get_height()
                )
        elif result == 'highscores':
            self.current_state = HighscoreState(
                self.screen.get_width(),
                self.screen.get_height(),
                self.engine.get_top_scores()
                )
        elif result == 'instructions':
            self.current_state = InstructionsState(
                self.screen.get_width(),
                self.screen.get_height()
                )
        elif result == 'quit':
            self.running = False
            pygame.quit()
            return