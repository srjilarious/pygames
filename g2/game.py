# Simple pygame program
import pygame
import math
import random

from pygame.locals import *

WindowWidth = 960
WindowHeight = 400
ScreenWidth = 240
ScreenHeight = 100
PlayerStartX = 25
PlayerStartY = 25

class GameContext:
    def __init__(self):
        # Set up the drawing window
        self.screen = pygame.display.set_mode([WindowWidth, WindowHeight], flags=HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.off_screen = pygame.surface.Surface((ScreenWidth, ScreenHeight))

        self.font = pygame.font.Font(None, 15)
        self.running = True
        self.player_x = PlayerStartX
        self.player_y = PlayerStartY
        self.player_radius = 8
        self.player_radius_sq = self.player_radius**2
        self.dot_radius = 4
        self.dot_radius_sq = self.dot_radius**2
        self.score = 1234
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
            self.player_y = max(self.player_radius, self.player_y - 0.1)
        if pressed_keys[K_DOWN]:
            self.player_y = min(self.player_y + 0.1,  ScreenHeight - self.player_radius)
        if pressed_keys[K_LEFT]:
            self.player_x = max(self.player_radius, self.player_x - 0.1)
        if pressed_keys[K_RIGHT]:
            self.player_x = min(self.player_x + 0.1, ScreenWidth - self.player_radius)
        if pressed_keys[K_RETURN]:
            self.player_x = PlayerStartX
            self.player_y = PlayerStartY
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
        self.off_screen.fill((0,0,0))

        # Draw a solid blue circle in the center
        pygame.draw.circle(self.off_screen, (0, 0, 255), (self.player_x, self.player_y), self.player_radius)

        # Draw the dots
        for i, dot in enumerate(self.dots):
            pygame.draw.circle(self.off_screen, (255, 255, 0), (dot[0], dot[1]), self.dot_radius)

        txt = self.font.render("Score: " + str(self.score), True, pygame.Color('white'))
        self.off_screen.blit(txt, (5, 5))

        self.screen.blit(pygame.transform.scale(self.off_screen, self.screen.get_rect().size), (0, 0))
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
            if event.type == QUIT:
                context.running = False
            elif event.type == VIDEORESIZE:
                context.screen = pygame.display.set_mode(event.size, flags=HWSURFACE|DOUBLEBUF|RESIZABLE)

        context.update_game()
        context.render()

    # Done! Time to quit.
    pygame.quit()