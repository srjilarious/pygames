
from .input import Keyboard
import arcade
from arcade.gl import geometry
from arcade.key import *
from pyglet.gl import *

class GameContext(arcade.Window):

    def __init__(self, win_size, screen_size, title):
        super().__init__(win_size[0], win_size[1], title)
        self.win_size = win_size
        self.screen_size = screen_size
        self.running = True
        self._game_state_paused = False
        self.game_states = {}
        self.curr_game_state_key = ""
        self.components = {}
        self.overlay_components = {}
        self.keyboard = Keyboard()
        self.setup_done = False
        self.scroll_x = 0
        self.scroll_y = 0

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

    def setup(self):
        self.setup_done = True

        for (k, v) in self.game_states.items():
            v.setup()

        for (k, v) in self.components.items():
            v.setup()

        for (k, v) in self.overlay_components.items():
            v.setup()

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        self.scroll_x = int(self.scroll_x)
        self.scroll_y = int(self.scroll_y)
        arcade.set_viewport(self.scroll_x, self.screen_size[0] + self.scroll_x, self.scroll_y, self.screen_size[1] + self.scroll_y)

        if self.setup_done:
            if self.curr_game_state is not None:
                self.curr_game_state.render()
            
            for (k, v) in self.components.items():
                if v.activated:
                    v.render()

            # Overlay components render at the window resolution
            if len(self.overlay_components) > 0:
                found_active_comp = False
                for (k, v) in self.overlay_components.items():
                    if v.activated:

                        # Only set the overlay component the first time we find an active overlay component
                        if not found_active_comp:
                            arcade.set_viewport(0, self.win_size[0], 0, self.win_size[1])
                            found_active_comp = True
                            
                        v.render()

    def on_update(self, delta_time):

        if self.curr_game_state is not None and not self.paused:
            self.curr_game_state.update(delta_time)

        for (k, v) in self.components.items():
            if v.activated:
                v.update(delta_time)

        for (k, v) in self.overlay_components.items():
            if v.activated:
                v.update(delta_time)

        self.keyboard.update()
        self.keyboard.post_update()

    def on_key_press(self, key, key_modifiers):
        self.keyboard.mark_text_key_down(key)
        self.keyboard.mark_pressed(key)

    def on_key_release(self, key, key_modifiers):
        self.keyboard.mark_text_key_up(key)
        self.keyboard.mark_released(key)

    