# Simple pygame program
import pygame
import math
import random
from pygame import time

from pygame.locals import *

WindowWidth = 1920
WindowHeight = 1080
ScreenWidth = 192
ScreenHeight = 108
PlayerStartX = 25
PlayerStartY = 25
Speed = 0.5

pygame.init()
RamonaSheet = pygame.image.load("ramona_test.png")

class Frame:
    def __init__(self, time, rect):
        self.time = time
        self.rect = rect
        self.surface = None

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = RamonaSheet

        self.frames = [ 
            Frame(200, (0, 182, 54, 67)),
            Frame(200, (54, 182, 54, 67)),
            Frame(200, (108, 182, 54, 67)),
            Frame(200, (162, 182, 54, 67)),
            Frame(200, (392, 0, 54, 67)),
            Frame(200, (216, 182, 54, 67)),
            Frame(200, (446, 0, 54, 67)),
            Frame(200, (270, 182, 54, 67)),
        ]

        for i, frame in enumerate(self.frames):
            frame.surface = self.sprite_sheet.subsurface(frame.rect)

        self.curr_frame_idx = 0
        self.curr_frame_time = 0
        self.position = (PlayerStartX, PlayerStartY)
        # self.rect = pygame.Rect(PlayerStartX, PlayerStartY, PlayerWidth, PlayerHeight)
        self.layer = 0

    @property 
    def curr_frame(self):
        return self.frames[self.curr_frame_idx]
    @property
    def image(self):
        return self.curr_frame.surface

    @property
    def rect(self):
        return pygame.Rect(self.position, (self.curr_frame.rect[2], self.curr_frame.rect[3]))

    def update(self, time_elapsed_ms):
        self.curr_frame_time += time_elapsed_ms
        if self.curr_frame_time > self.curr_frame.time:
            self.curr_frame_time -= self.curr_frame.time
            self.curr_frame_idx += 1
            if self.curr_frame_idx >= len(self.frames):
                self.curr_frame_idx = 0
        

class GameContext:
    def __init__(self):
        # Set up the drawing window
        self.screen = pygame.display.set_mode([WindowWidth, WindowHeight], flags=HWSURFACE|DOUBLEBUF)
        self.off_screen = pygame.surface.Surface((ScreenWidth, ScreenHeight))

        self.player = Player()
        self.font = pygame.font.Font(None, 15)
        self.running = True

        if pygame.joystick.get_count() > 0:
            self.joystick = joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None


    def move_up(self):
        self.player.rect = self.player.rect.move(0, -Speed)

    def move_down(self):
        self.player.rect = self.player.rect.move(0, Speed)

    def move_left(self):
        self.player.rect = self.player.rect.move(-Speed, 0)

    def move_right(self):
        self.player.rect = self.player.rect.move(Speed, 0)

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

        self.player.update(10)

    def render(self):
        # Fill the background with white
        self.off_screen.fill((0,0,0))

        # Draw sprite to off_screen buffer
        self.off_screen.blit(self.player.image, self.player.rect)

        self.screen.blit(pygame.transform.scale(self.off_screen, self.screen.get_rect().size), (0, 0))
        # Flip the display
        pygame.display.flip()


if __name__ == "__main__":
    pygame.joystick.init()

    context = GameContext()
    


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