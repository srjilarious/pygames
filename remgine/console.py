from remgine.game_component import GameComponent
import pygame as pg

class Console(GameComponent):

    def __init__(self, context, font=None):
        GameComponent.__init__(self, context)
        self._context = context
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
            txt = self.font.render("What an awesome Console!!!", False, pg.Color('white'))
            self._context.off_screen.blit(txt, (5, 5))
