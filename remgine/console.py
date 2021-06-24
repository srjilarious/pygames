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
        self._line = ""

    def update(self):
        self._line += self._context.keyboard.text_buffer

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

            txt = self.font.render(self._line, False, pg.Color('white'))
            self._console_surf.blit(txt, (5, 5))
            self._context.screen.blit(self._console_surf, (0, 0))
