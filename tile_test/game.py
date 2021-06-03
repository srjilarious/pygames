# Simple pygame program
import pygame
import math
import random

from pygame.locals import *
import pytmx
from pytmx.util_pygame import load_pygame
import pyscroll

WindowWidth = 1920
WindowHeight = 1080
ScreenWidth = 768
ScreenHeight = 432
PlayerStartX = 25
PlayerStartY = 25
PlayerWidth = 16
PlayerHeight = 16
Speed = 2

class GameContext:
    def __init__(self):
        # Set up the drawing window
        self.screen = pygame.display.set_mode([WindowWidth, WindowHeight], flags=HWSURFACE|DOUBLEBUF)
        self.off_screen = pygame.surface.Surface((ScreenWidth, ScreenHeight))

        self.font = pygame.font.Font(None, 15)
        self.running = True
        self.score = 1234
        
        self.player_rect = pygame.Rect(PlayerStartX, PlayerStartY, PlayerWidth, PlayerHeight)
        self.tmxdata = load_pygame("level1.tmx")
        self.map_data = pyscroll.TiledMapData(self.tmxdata)
        self.main_tiles = self.tmxdata.get_layer_by_name("main_layer")
        
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, (ScreenWidth, ScreenHeight), clamp_camera=False)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        if pygame.joystick.get_count() > 0:
            self.joystick = joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None
        self.debug_rects = []

    def move_up(self):
        # self.player_y = max(self.player_radius, self.player_y - Speed)
        new_rect = self.player_rect.move(0, -Speed)
        ty = int(new_rect.top / self.tmxdata.tileheight)
        tx_l = int(new_rect.left / self.tmxdata.tilewidth)
        tx_r = int(new_rect.right / self.tmxdata.tilewidth)
        if not self.check_collide_tile(new_rect, tx_l, ty) and not self.check_collide_tile(new_rect, tx_r, ty):
            self.player_rect = new_rect
        
    def move_down(self):
        new_rect = self.player_rect.move(0, Speed)
        ty = int(new_rect.bottom / self.tmxdata.tileheight)
        tx_l = int(new_rect.left / self.tmxdata.tilewidth)
        tx_r = int(new_rect.right / self.tmxdata.tilewidth)
        if not self.check_collide_tile(new_rect, tx_l, ty) and not self.check_collide_tile(new_rect, tx_r, ty):
            self.player_rect = new_rect

    def move_left(self):
        new_rect = self.player_rect.move(-Speed, 0)
        tx = int(new_rect.left / self.tmxdata.tilewidth)
        ty_t = int(new_rect.top / self.tmxdata.tileheight)
        ty_b = int(new_rect.bottom / self.tmxdata.tileheight)
        if not self.check_collide_tile(new_rect, tx, ty_t) and not self.check_collide_tile(new_rect, tx, ty_b):
            self.player_rect = new_rect

    def move_right(self):
        new_rect = self.player_rect.move(Speed, 0)
        tx = int(new_rect.right / self.tmxdata.tilewidth)
        ty_t = int(new_rect.top / self.tmxdata.tileheight)
        ty_b = int(new_rect.bottom / self.tmxdata.tileheight)
        if not self.check_collide_tile(new_rect, tx, ty_t) and not self.check_collide_tile(new_rect, tx, ty_b):
            self.player_rect = new_rect

    def update_game(self):
        pressed_keys = pygame.key.get_pressed()

        if (pressed_keys[K_UP] or 
            pressed_keys[K_DOWN] or
            pressed_keys[K_LEFT] or
            pressed_keys[K_RIGHT]):
            self.debug_rects.clear()

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

        # Handle joystick input
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

        
    def check_collide_tile(self, player_rect, x, y):
        tile = self.get_main_tile(x, y)
        tw = self.tmxdata.tilewidth
        th = self.tmxdata.tileheight
        if tile != 0:
            collide_rect = pygame.Rect(int(x*tw), int(y*th), tw, th)
            # Debug, draw collide rect.
            self.debug_rects.append(collide_rect)

            return player_rect.colliderect(collide_rect)
        else:
            return False

    def get_main_tile(self, x, y):
        return self.main_tiles.data[int(y)][int(x)]

    def render(self):
        # Fill the background with white
        # self.off_screen.fill((0,0,0))


        self.group.center((self.player_rect.x, self.player_rect.y))
        #self.group.center((ScreenWidth/2, ScreenHeight/2))
        self.group.draw(self.off_screen)
        
        # Draw a solid blue circle in the center
        # pygame.draw.circle(self.off_screen, (0, 0, 255), (self.player_x, self.player_y), self.player_radius)
        p_screen_pos = pygame.Rect(ScreenWidth/2, ScreenHeight/2, PlayerWidth, PlayerHeight)
        pygame.draw.rect(self.off_screen, (0,0,255), p_screen_pos)
        #pygame.draw.rect(self.off_screen, (0,0,255), self.player_rect)

        map_offset = (self.player_rect.x-ScreenWidth/2, self.player_rect.y-ScreenHeight/2)
        for r in self.debug_rects:
            pygame.draw.rect(self.off_screen, (255,255,255), r.move((-map_offset[0], -map_offset[1])), width=1)

        txt = self.font.render("Score: " + str(self.score), False, pygame.Color('white'))
        self.off_screen.blit(txt, (5, 5))

        self.screen.blit(pygame.transform.scale(self.off_screen, self.screen.get_rect().size), (0, 0))
        # Flip the display
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
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