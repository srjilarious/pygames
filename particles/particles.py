import sys
sys.path.append("..")

import arcade
from arcade.key import *

import remgine
import remgine.console

import random

WindowWidth = 1280
WindowHeight = 720
ScreenWidth = 384
ScreenHeight = 216

NumParticlesPerExplosion = 100

class Particle:
    def __init__(self, position=(ScreenWidth/2,ScreenHeight/2)):
        self.speed = (random.random()*5-2.5, random.random()*5-2.5)
        self.time_left_ms = random.randint(500, 2000)
        self.color = (random.randint(10, 255), random.randint(10, 255), random.randint(100, 160), 255)
        self.position = position

    def update(self, time_elapsed):
        self.position = (self.position[0] + self.speed[0], self.position[1] + self.speed[1])
        self.time_left_ms -= time_elapsed
        self.color = (self.color[0], self.color[1], self.color[2], min(255, self.time_left_ms/20))
        return self.time_left_ms > 0

    def render(self):
        arcade.draw_rectangle_filled(self.position[0], self.position[1], 4, 4, self.color)


class Explosion:
    def __init__(self, position, numParticles=NumParticlesPerExplosion):
        self.particles = []
        for i in range(numParticles):
            self.particles.append(Particle(position))

    def update(self, time_elapsed_ms):
        parts = []
        for p in self.particles:
            if p.update(time_elapsed_ms):
                parts.append(p)
        self.particles = parts
        return len(parts) > 0

    def render(self):
        print(f"Drawing {len(self.particles)} particles")
        l = arcade.ShapeElementList()
        for p in self.particles:
            l.append(arcade.create_rectangle_filled(p.position[0], p.position[1], 4, 4, p.color))
        l.draw()

class MainState(remgine.GameState):
    def __init__(self, context):
        remgine.GameState.__init__(self, context)
        
        # self.font = pg.font.Font(None, 15)
        self.running = True
        self.score = 0
        
        self.explosions = [] #pg.sprite.Group()

    def update(self):
        kb = self.context.keyboard
        if kb.down(SPACE):
            self.explosions.append(Explosion(position=(random.randint(20, ScreenWidth-20), random.randint(20, ScreenHeight-20))))

        if kb.down(ESCAPE):
            self.running = False

        exp = []
        for e in self.explosions:
            if e.update(10):
                exp.append(e)
        self.explosions = exp

    def render(self):
        for e in self.explosions:
            e.render()

if __name__ == "__main__":
    
    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight),
            title="Game State Example"
        )
    
    context.game_states["main_state"] = MainState(context)
    context.curr_game_state_key = "main_state"
    # context.components["global_keys"] = StateComponent(context)

    arcade.run()
    