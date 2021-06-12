
from .input import Keyboard
import pygame as pg
from pygame.locals import *

class GameContext:

    def __init__(self, win_size, screen_size):
        self.win_size = win_size
        self.screen_size = screen_size

        self.screen = pg.display.set_mode([win_size[0], win_size[1]], flags=HWSURFACE|DOUBLEBUF)
        self.off_screen = pg.surface.Surface((screen_size[0], screen_size[1]))

        self.running = True
        self.game_states = {}
        self.curr_game_state_key = ""

        self.keyboard = Keyboard()

    @property
    def curr_game_state(self):
        return self.game_states.get(self.curr_game_state_key, None)

    def update(self):
        self.keyboard.update()

        if self.curr_game_state is not None:
            self.curr_game_state.update()

    def render(self):
        if self.curr_game_state is not None:
            self.curr_game_state.render()
        
        self.screen.blit(pg.transform.scale(self.off_screen, self.screen.get_rect().size), (0, 0))
        # Flip the display
        pg.display.flip()
    