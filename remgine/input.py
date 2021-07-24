# A class for input related classes
import collections
import arcade.key as key

class Keyboard():

    def __init__(self):
        self._down_keys = {}
        self._last_down_keys = {}
        self._text_keys = collections.defaultdict()
        self.text_buffer = []

    def update(self):
        self._last_down_keys = self._down_keys.copy()

    def post_update(self):
        self.text_buffer = []

    def mark_text_key_down(self, k):
        if k is None:
            return
        
        if k not in self._text_keys:
            # print(f"Adding key '{k.unicode}' to text buffer")
            self.text_buffer.append(k)

        # Rest any timing for this key.
        self._text_keys[k] = (k, 0)
    
    def mark_text_key_up(self, k):
        del self._text_keys[k]

    def mark_pressed(self, k):
        self._down_keys[k] = True

    def mark_released(self, k):
        self._down_keys[k] = False

    def up(self, key):
        return not self._down_keys.get(key, False)

    def down(self, key):
        return self._down_keys.get(key, False)

    def any_down(self, keys):
        for k in keys:
            if self.down(k):
                return True
        return False
    
    def pressed(self, key):
        return self._down_keys.get(key, False) and not self._last_down_keys.get(key, False)

    def any_pressed(self, keys):
        for k in keys:
            if self.pressed(k):
                return True
        return False
    
    def released(self, key):
        return not self._down_keys.get(key, False) and self._last_down_keys.get(key, False)

