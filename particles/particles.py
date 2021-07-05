import sys
sys.path.append("..")

import pygame as pg
from pygame.locals import *

import remgine
import remgine.console

import random

WindowWidth = 1280
WindowHeight = 720
ScreenWidth = 384
ScreenHeight = 216

NumParticlesPerExplosion = 100

class Particle(pg.sprite.Sprite):
    def __init__(self, position=(ScreenWidth/2,ScreenHeight/2)):
        pg.sprite.Sprite.__init__(self)
        self.speed = (random.random()*10-5, random.random()*10-5)
        self.time_left_ms = random.randint(500, 2000)
        self.color = (random.randint(10, 255), random.randint(10, 255), random.randint(10, 255), 255)
        self.position = position

    def update(self, time_elapsed):
        self.position = (self.position[0] + self.speed[0], self.position[1] + self.speed[1])
        self.time_left_ms -= time_elapsed
        return self.time_left_ms > 0

    def render(self, surface):
        pg.draw.rect(surface, self.color, pg.Rect(self.position[0], self.position[1], 4, 4))


class Explosion:
    def __init__(self, numParticles=NumParticlesPerExplosion):
        self.particles = []
        for i in range(numParticles):
            self.particles.append(Particle())

    def update(self, time_elapsed_ms):
        parts = []
        for p in self.particles:
            if p.update(time_elapsed_ms):
                parts.append(p)
        self.particles = parts
        return len(parts) > 0
    def render(self, surface):
        print(f"Drawing {len(self.particles)} particles")
        for p in self.particles:
            p.render(surface)

class MainState(remgine.GameState):
    def __init__(self, context):
        remgine.GameState.__init__(self, context)
        
        self.font = pg.font.Font(None, 15)
        self.running = True
        self.score = 0
        
        self.explosions = [] #pg.sprite.Group()

    def update(self):
        kb = self.context.keyboard
        if kb.pressed(K_SPACE):
            self.explosions.append(Explosion())

        if kb.down(K_ESCAPE):
            self.running = False

        exp = []
        for e in self.explosions:
            if e.update(10):
                exp.append(e)
        self.explosions = exp

    def render(self):
        self.context.off_screen.fill((0,0,0))
        for e in self.explosions:
            e.render(self.context.off_screen)

if __name__ == "__main__":
    
    context = remgine.GameContext(
        win_size=(WindowWidth, WindowHeight), 
        screen_size=(ScreenWidth, ScreenHeight)
    )
    context.game_states["main_state"] = MainState(context)
    context.curr_game_state_key = "main_state"

    # console = remgine.console.Console(context)
    # context.overlay_components["console"] = console

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