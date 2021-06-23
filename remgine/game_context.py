
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
        self._game_state_paused = False
        self.game_states = {}
        self.components = {}
        self.overlay_components = {}

        self.curr_game_state_key = ""

        self.keyboard = Keyboard()

    @property
    def curr_game_state(self):
        return self.game_states.get(self.curr_game_state_key, None)

    @property
    def paused(self):
        return self._game_state_paused
    
    @paused.setter
    def paused(self, value):
        self._game_state_paused = value
        if self.curr_game_state is not None:
            self.curr_game_state.on_pause_changed(value)

    def update(self):
        self.keyboard.update()

        if self.curr_game_state is not None and not self.paused:
            self.curr_game_state.update()

        for (k, v) in self.components.items():
            v.update()
            
        for (k, v) in self.overlay_components.items():
            v.update()

    def render(self):
        if self.curr_game_state is not None:
            self.curr_game_state.render()
        
        for (k, v) in self.components.items():
            v.render()

        self.screen.blit(pg.transform.scale(self.off_screen, self.screen.get_rect().size), (0, 0))
        
        # Overlay components render at the window resolution
        for (k, v) in self.overlay_components.items():
            v.render()

        # Flip the display
        pg.display.flip()
    