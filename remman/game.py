import sys
sys.path.append("..")

import pygame as pg
from pygame.locals import *

import remgine
from play_state import PlayState

from constants import *

if __name__ == "__main__":
    
    context = remgine.GameContext(
        win_size=(WindowWidth, WindowHeight), 
        screen_size=(ScreenWidth, ScreenHeight)
    )
    context.game_states["play_state"] = PlayState(context)

    context.curr_game_state_key = "play_state"
    while context.running:
        # Did the user click the window close button?
        for event in pg.event.get():
            if event.type == QUIT:
                context.running = False
            elif event.type == VIDEORESIZE:
                context.screen = pg.display.set_mode(event.size, flags=HWSURFACE|DOUBLEBUF)

        context.update()
        context.render()

        if context.keyboard.pressed(K_ESCAPE):
            context.running = False

    # Done! Time to quit.
    pg.quit()