# A class for input related classes

import pygame
from pygame.locals import *

class Keyboard():

    def __init__(self):
        self._down_keys = pygame.key.get_pressed()
        self._last_down_keys = pygame.key.get_pressed()

    def update(self):
        self._last_down_keys = self._down_keys
        self._down_keys = pygame.key.get_pressed()

    def up(self, key):
        return not self._down_keys[key]

    def down(self, key):
        return self._down_keys[key]

    def any_down(self, keys):
        for k in keys:
            if self.down(k):
                return True
        return False
    
    def pressed(self, key):
        return self._down_keys[key] and not self._last_down_keys[key]

    def any_pressed(self, keys):
        for k in keys:
            if self.pressed(k):
                return True
        return False
    
    def released(self, key):
        return not self._down_keys[key] and self._last_down_keys[key]

