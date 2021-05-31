# Simple pygame program
import pygame
import math
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_ESCAPE,
    K_h,
    K_c,
    KEYDOWN,
    QUIT,
)

ScreenWidth = 160
ScreenHeight = 90


class GameContext:
    def __init__(self):
        # Set up the drawing window
        self.screen = pygame.display.set_mode([ScreenWidth, ScreenHeight], flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SCALED)
        self.font = pygame.font.Font(None, 20)
        self.running = True
        self.player_x = 25 
        self.player_y = 25
        self.player_radius = 5
        self.player_radius_sq = self.player_radius**2
        self.dot_radius = 4
        self.dot_radius_sq = self.dot_radius**2
        self.score = 0
        self.dots = []

    def create_dot(self):
        if len(self.dots) < 5000:
            self.dots += [(random.randint(0, ScreenWidth), random.randint(0, ScreenHeight))]

    def check_collide(self, dot):
        dist_sq = (dot[0] - self.player_x)**2 + (dot[1] - self.player_y)**2
        if dist_sq < (self.dot_radius_sq + self.player_radius_sq):
            return True
        return False


    def update_game(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            self.player_y = max(-2*ScreenHeight, self.player_y - 0.1)
        if pressed_keys[K_DOWN]:
            self.player_y = min(self.player_y + 0.1,  2*ScreenHeight)
        if pressed_keys[K_LEFT]:
            self.player_x = max(-2*ScreenHeight, self.player_x - 0.1)
        if pressed_keys[K_RIGHT]:
            self.player_x = min(self.player_x + 0.1, 2*ScreenHeight)
        if pressed_keys[K_RETURN]:
            self.player_x = 25
            self.player_y = 25
        if pressed_keys[K_h]:
            self.create_dot()
        if pressed_keys[K_c]:
            self.dots.clear()
        if pressed_keys[K_ESCAPE]:
            self.running = False

        # Check collisions with dots
        for i, dot in enumerate(self.dots):
            if self.check_collide(dot):
                self.score += 50
                del self.dots[i]

    def render(self):
        # Fill the background with white
        self.screen.fill((0,0,0))

        # Draw a solid blue circle in the center
        pygame.draw.circle(self.screen, (0, 0, 255), (self.player_x, self.player_y), self.player_radius)

        # Draw the dots
        for i, dot in enumerate(self.dots):
            pygame.draw.circle(self.screen, (255, 255, 0), (dot[0], dot[1]), self.dot_radius)

        txt = self.font.render("Score: " + str(self.score), True, pygame.Color('white'))
        self.screen.blit(txt, (5, 5))
        # Flip the display
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    context = GameContext()
    
    for i in range(100):
        context.create_dot()

    while context.running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                context.running = False

        ticks = pygame.time.get_ticks()
        context.update_game()
        context.render()
        
        new_ticks = pygame.time.get_ticks()
        delta_ticks = new_ticks = ticks
        if delta_ticks < (1000/30):
            pygame.time.wait((1000/30) - delta_ticks)


    # Done! Time to quit.
    pygame.quit()