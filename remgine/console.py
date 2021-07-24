import os

import arcade
import arcade.key as key

from remgine.game_component import GameComponent

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
DEFAULT_FONT_NAME=os.path.join(SCRIPT_ROOT, "..", "assets", "Inconsolata-Regular.ttf")

class Console(GameComponent):

    def __init__(self, context, font_name=None):
        GameComponent.__init__(self, context)
        self._context = context
        width = context.win_size[0]
        height = context.win_size[1]
        self._console_bg = arcade.create_rectangle_filled(width/2, int(3*height/4), width, height/2, (40, 40, 220, 180))
        self.lines = []
        self._line_render_offset = 0
        self._line = ""
        self.font_name = font_name or DEFAULT_FONT_NAME

    def update(self, delta_time):
        kb = self._context.keyboard

        for k in self._context.keyboard.text_buffer:
        #     # if k.mod == KMOD_NONE:
            if k == key.BACKSPACE:
                self._line = self._line[:-1]
            elif k == key.ENTER:
                self.lines.append(self._line)
                self._line = ""
            elif k == key.UP:
                if self._line_render_offset < len(self.lines):
                    self._line_render_offset += 1
            elif k == key.DOWN:
                if self._line_render_offset > 0:
                    self._line_render_offset -= 1
            elif k == key.END:
                self._line_render_offset = 0
            elif k != '':
                self._line += chr(k)

    @property
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, value):
        self._activated = value

        # Pause the game once the console comes up.
        self.context.paused = value

    def render(self):
        if self.activated:
            self._console_bg.draw()

            # Draw the input line at the bottom first
            curr_y = int(self._context.win_size[1]/2)
            text = arcade.draw_text(self._line, 
                            2, curr_y, 
                            (220, 220, 50), 
                            font_size=25,
                            font_name=self.font_name)

            curr_y += text.height

            for l in reversed(self.lines[:len(self.lines)-self._line_render_offset]):
                text = arcade.draw_text(l, 
                            2, curr_y, 
                            (120, 255, 255), 
                            font_size=25,
                            font_name=self.font_name)
                curr_y += text.height

                if(curr_y > self.context.win_size[1]+text.height):
                    break
