from remgine.game_component import GameComponent
import pygame as pg

class Console(GameComponent):

    def __init__(self, context, font=None):
        GameComponent.__init__(self, context)
        self._context = context
        self._console_surf = pg.Surface((context.screen_size[0],context.screen_size[1]), pg.SRCALPHA) 
        self.font = font
        if self.font is None:
            self.font = pg.font.Font(None, 20)

    def update(self):
        pass

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
                    self._context.screen_size[0], 
                    int(self._context.screen_size[1]/2)
                )
            pg.draw.rect(self._console_surf, (40, 40, 220, 180), console_rect)

            txt = self.font.render("What an awesome Console!!!", False, pg.Color('white'))
            self._console_surf.blit(txt, (5, 5))
            self._context.off_screen.blit(self._console_surf, (0, 0))
