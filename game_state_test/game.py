import pygame as pg
from pygame.locals import *

import sys
sys.path.append("..")
import remgine

WindowWidth = 1920
WindowHeight = 1080
ScreenWidth = 192
ScreenHeight = 108


class BlueState(remgine.GameState):
    def __init__(self, context):
        remgine.GameState.__init__(self, context)

    def render(self):
        # Fill the background with white
        self.context.off_screen.fill((0,0,255))

class RedState(remgine.GameState):
    def __init__(self, context):
        remgine.GameState.__init__(self, context)

    def render(self):
        # Fill the background with white
        self.context.off_screen.fill((255,0,0))

if __name__ == "__main__":
    # pygame.joystick.init()

    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight)
        )
    
    context.game_states["blue"] = BlueState(context)
    context.game_states["red"] = RedState(context)
    context.curr_game_state_key = "blue"

    while context.running:
        # Did the user click the window close button?
        for event in pg.event.get():
            if event.type == QUIT:
                context.running = False
            elif event.type == VIDEORESIZE:
                context.screen = pg.display.set_mode(event.size, flags=HWSURFACE|DOUBLEBUF)

        context.update()
        if context.keyboard.released(K_F1):
            context.curr_game_state_key = "blue"
        elif context.keyboard.released(K_F2):
            context.curr_game_state_key = "red"

        context.render()

    # Done! Time to quit.
    pg.quit()