from pygame.constants import (
        K_BACKSPACE, KMOD_NONE, K_RETURN, K_UP, K_DOWN, K_END
    )
from remgine.game_component import GameComponent
import pygame as pg

class Console(GameComponent):

    def __init__(self, context, font=None):
        GameComponent.__init__(self, context)
        self._context = context
        self._console_surf = pg.Surface((context.win_size[0],context.win_size[1]), pg.SRCALPHA) 
        self.font = font
        if self.font is None:
            self.font = pg.font.Font("assets/AmigaTopaz.ttf", 30)
        self.lines = []
        self._line_render_offset = 0
        self._line = ""

    def update(self):
        for k in self._context.keyboard.text_buffer:
            # if k.mod == KMOD_NONE:
            if k.key == K_BACKSPACE:
                self._line = self._line[:-1]
            elif k.key == K_RETURN:
                self.lines.append(self._line)
                self._line = ""
            elif k.key == K_UP:
                if self._line_render_offset < len(self.lines):
                    self._line_render_offset += 1
            elif k.key == K_DOWN:
                if self._line_render_offset > 0:
                    self._line_render_offset -= 1
            elif k.key == K_END:
                self._line_render_offset = 0
            elif k.unicode != '':
                self._line += k.unicode

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
            console_rect = pg.Rect(
                    0, 0, 
                    self._context.win_size[0], 
                    int(self._context.win_size[1]/2)
                )
            pg.draw.rect(self._console_surf, (40, 40, 220, 180), console_rect)

            # Draw the input line at the bottom first
            txt = self.font.render(self._line, False, pg.Color('white'))
            curr_y = int(self._context.win_size[1]/2) - txt.get_size()[1]
            self._console_surf.blit(txt, (5, curr_y))

            for l in reversed(self.lines[:len(self.lines)-self._line_render_offset]):
                txt = self.font.render(l, False, pg.Color('white'))
                curr_y -= int(txt.get_size()[1])
                self._console_surf.blit(txt, (5, curr_y))

                if(curr_y < -txt.get_size()[1]):
                    break

            self._context.screen.blit(self._console_surf, (0, 0))
