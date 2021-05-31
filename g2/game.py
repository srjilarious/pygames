# Simple pygame program
import pygame
import math
import random

from pygame.locals import *

WindowWidth = 1920
WindowHeight = 1080
ScreenWidth = 192
ScreenHeight = 108
PlayerStartX = 25
PlayerStartY = 25
Speed = 0.5

class GameContext:
    def __init__(self):
        # Set up the drawing window
        self.screen = pygame.display.set_mode([WindowWidth, WindowHeight], flags=HWSURFACE|DOUBLEBUF)
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

        if pygame.joystick.get_count() > 0:
            self.joystick = joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def create_dot(self):
        if len(self.dots) < 5000:
            self.dots += [(random.randint(0, ScreenWidth), random.randint(0, ScreenHeight))]

    def check_collide(self, dot):
        dist_sq = (dot[0] - self.player_x)**2 + (dot[1] - self.player_y)**2
        if dist_sq < (self.dot_radius_sq + self.player_radius_sq):
            return True
        return False


    def move_up(self):
        self.player_y = max(self.player_radius, self.player_y - Speed)

    def move_down(self):
        self.player_y = min(self.player_y + Speed,  ScreenHeight - self.player_radius)

    def move_left(self):
        self.player_x = max(self.player_radius, self.player_x - Speed)

    def move_right(self):
        self.player_x = min(self.player_x + Speed, ScreenWidth - self.player_radius)

    def update_game(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            self.move_up()
        if pressed_keys[K_DOWN]:
            self.move_down()
        if pressed_keys[K_LEFT]:
            self.move_left()
        if pressed_keys[K_RIGHT]:
            self.move_right()
        if pressed_keys[K_RETURN]:
            self.player_x = PlayerStartX
            self.player_y = PlayerStartY
        if pressed_keys[K_h]:
            self.create_dot()
        if pressed_keys[K_c]:
            self.dots.clear()
        if pressed_keys[K_ESCAPE]:
            self.running = False


        if self.joystick is not None:
            jx, jy = self.joystick.get_hat(0)
            if jy > 0:
                self.move_up()
            if jy < 0:
                self.move_down()
            if jx < 0:
                self.move_left()
            if jx > 0:
                self.move_right()

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

        txt = self.font.render("Score: " + str(self.score), False, pygame.Color('white'))
        self.off_screen.blit(txt, (5, 5))

        self.screen.blit(pygame.transform.scale(self.off_screen, self.screen.get_rect().size), (0, 0))
        # Flip the display
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()

    context = GameContext()
    
    for i in range(100):
        context.create_dot()

    while context.running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == QUIT:
                context.running = False
            elif event.type == VIDEORESIZE:
                context.screen = pygame.display.set_mode(event.size, flags=HWSURFACE|DOUBLEBUF)

        context.update_game()
        context.render()

    # Done! Time to quit.
    pygame.quit()