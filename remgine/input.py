# A class for input related classes

import pygame
import collections
from pygame.locals import *

class Keyboard():

    def __init__(self):
        self._down_keys = pygame.key.get_pressed()
        self._last_down_keys = pygame.key.get_pressed()
        self._text_keys = collections.defaultdict()
        self.text_buffer = []

    def update(self):
        self._last_down_keys = self._down_keys
        self._down_keys = pygame.key.get_pressed()

    def post_update(self):
        self.text_buffer = []

    def mark_text_key_down(self, k):
        if k.unicode is None:
            return
        
        if k.key not in self._text_keys:
            # print(f"Adding key '{k.unicode}' to text buffer")
            self.text_buffer.append(k)

        # Rest any timing for this key.
        self._text_keys[k.key] = (k, 0)
    
    def mark_text_key_up(self, k):
        del self._text_keys[k.key]

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

