import sys
sys.path.append("..")

import pygame as pg
from pygame.locals import *

import remgine
import remgine.console

from play_state import PlayState

from constants import *

if __name__ == "__main__":
    
    context = remgine.GameContext(
        win_size=(WindowWidth, WindowHeight), 
        screen_size=(ScreenWidth, ScreenHeight)
    )
    context.game_states["play_state"] = PlayState(context)
    context.curr_game_state_key = "play_state"

    console = remgine.console.Console(context)
    context.overlay_components["console"] = console

    while context.running:

        # Did the user click the window close button?
        for event in pg.event.get():
            if event.type == QUIT:
                context.running = False
            elif event.type == VIDEORESIZE:
                context.screen = pg.display.set_mode(event.size, flags=HWSURFACE|DOUBLEBUF)
            elif event.type == KEYDOWN:
                context.keyboard.mark_text_key_down(event)
            elif event.type == KEYUP:
                context.keyboard.mark_text_key_up(event)

        context.update()
        context.render()

        if context.keyboard.pressed(K_ESCAPE):
            context.running = False
        if context.keyboard.pressed(K_BACKQUOTE):
            console.activated = not console.activated

    # Done! Time to quit.
    pg.quit()