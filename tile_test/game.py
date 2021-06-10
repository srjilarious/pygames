# Tile engine pygame test
import math
import random
import importlib
import logging
import sys

import pygame
from pygame.locals import *

import pytmx
from pytmx.util_pygame import load_pygame
import pyscroll

sys.path.append("..")
import remgine

WindowWidth = 1920
WindowHeight = 1080
ScreenWidth = 768
ScreenHeight = 432
PlayerStartX = 64
PlayerStartY = 64
PlayerWidth = 32
PlayerHeight = 32
Speed = 2

pygame.init()
BluePiece = pygame.image.load("blue_piece.png")
SpriteSheet = pygame.image.load("game_content5.png")

def midpoint(a, b):
        return int(a + (b-a)/2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(BluePiece, (PlayerWidth, PlayerHeight))
        self.rect = pygame.Rect(PlayerStartX, PlayerStartY, PlayerWidth, PlayerHeight)
        self.layer = 0

class GameContext:
    def __init__(self):
        # Set up the drawing window
        self.screen = pygame.display.set_mode([WindowWidth, WindowHeight], flags=HWSURFACE|DOUBLEBUF)
        self.off_screen = pygame.surface.Surface((ScreenWidth, ScreenHeight))

        self.font = pygame.font.Font(None, 15)
        self.running = True
        self.score = 0
        
        self.keyboard = remgine.Keyboard()

        
        self.player = remgine.Actor({
            "standing": remgine.Frames(SpriteSheet, 
            [ 
                remgine.Frame(400, (557, 0, 42, 65)),
                remgine.Frame(400, (557, 68, 42, 65), (1, 0), (-1, 0)),
            ]),
            "walking": remgine.Frames(SpriteSheet, 
            [ 
                remgine.Frame(200, (368, 296, 50, 65)),
                remgine.Frame(200, (302, 358, 50, 65)),
                remgine.Frame(200, (420, 256, 50, 65)),
                remgine.Frame(200, (354, 363, 50, 65)),
                remgine.Frame(200, (420, 323, 50, 65)),
                remgine.Frame(200, (406, 390, 50, 65)),
                remgine.Frame(200, (458, 390, 50, 65)),
                remgine.Frame(200, (505, 0, 50, 65)),
            ])
        }, "standing", (100, 100))
        self.player.collide_adjust = (0, 0, 50, 60)

        self.CoinFrames = remgine.Frames(SpriteSheet, [
            remgine.Frame(400, (0, 448, 16, 16)),
            remgine.Frame(400, (18, 448, 16, 16)),
            remgine.Frame(400, (36, 448, 16, 16)),
            remgine.Frame(400, (54, 448, 16, 16)),
        ])

        self.tmxdata = load_pygame("level1.tmx")

        level_script = self.tmxdata.properties["start_script"]
        if level_script is not None:
            print("Got a level script from the level: " + level_script)
            level_module = importlib.import_module(level_script)
            level_module.start()
        self.map_data = pyscroll.TiledMapData(self.tmxdata)
        self.main_tiles = self.tmxdata.get_layer_by_name("main_layer")
        
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, (ScreenWidth, ScreenHeight), clamp_camera=False)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        self.group.add(self.player)

        # Create an object grid and register our map objects into it.
        self.collectible_obj_grid = self.create_obj_grid("collectible_objects")
        self.interaction_obj_grid = self.create_obj_grid("interaction_objects")
        
        if pygame.joystick.get_count() > 0:
            self.joystick = joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None
        self.debug_rects = []

    def create_obj_grid(self, layer_name):
        obj_grid = remgine.ObjectGrid(self.tmxdata.width, self.tmxdata.height, self.tmxdata.tilewidth, self.tmxdata.tileheight)
        obj_group = self.tmxdata.get_layer_by_name(layer_name)
        for obj in obj_group:
            print("Inserting object {} at {}, {} with name {}, from {}".format(obj.name, obj.x, obj.y, obj.name, layer_name))
            if obj.name == "coin":
                obj.sprite = remgine.Actor({"normal": self.CoinFrames}, "normal", (obj.x, obj.y))
                obj.sprite.scale = 2
                self.group.add(obj.sprite)

            obj_grid.insert_obj((obj.x, obj.y, obj.width, obj.height), obj)

        return obj_grid

    def check_obj_collisions(self, objs):
        if len(objs) > 0:
            for o in objs:
                print("Hit object: " + o.name)
                if o.name == "coin" and o.sprite in self.group:
                    self.score += 100
                    self.group.remove(o.sprite)

    # def tile_pos(self, point):
    #     return (int(point[0] / self.tmxdata.tilewidth), int(point[1] / self.tmxdata.tileheight))

    def move_up(self):
        # self.player_y = max(self.player_radius, self.player_y - Speed)
        new_rect = self.player.collide_rect.move(0, -Speed)
        ty = int(new_rect.top / self.tmxdata.tileheight)
        tx_l = int(new_rect.left / self.tmxdata.tilewidth)
        tx_r = int(new_rect.right / self.tmxdata.tilewidth)
        if not self.check_collide_tile(new_rect, tx_l, ty) and not self.check_collide_tile(new_rect, tx_r, ty):
            self.player.position = (new_rect.x, new_rect.y)
        #     self.player.position = (self.player.position[0], self.player.position[1] -Speed)
        # else:
        #     self.player.position = (self.player.position[0], (ty+1)*self.tmxdata.tileheight)

        # Check object collisions
        self.check_obj_collisions(self.collectible_obj_grid.get(tx_l, ty))
        self.check_obj_collisions(self.collectible_obj_grid.get(midpoint(tx_l, tx_r), ty))
        self.check_obj_collisions(self.collectible_obj_grid.get(tx_r, ty))
        
        
    def move_down(self):
        new_rect = self.player.collide_rect.move(0, Speed)
        ty = int(new_rect.bottom / self.tmxdata.tileheight)
        tx_l = int(new_rect.left / self.tmxdata.tilewidth)
        tx_r = int(new_rect.right / self.tmxdata.tilewidth)
        if not self.check_collide_tile(new_rect, tx_l, ty) and not self.check_collide_tile(new_rect, tx_r, ty):
            self.player.position = (new_rect.x, new_rect.y)
        #     self.player.position = (self.player.position[0], self.player.position[1] +Speed)
        # else:
        #     self.player.position = (self.player.position[0], (ty-1)*self.tmxdata.tileheight-1)
        
        # Check object collisions
        self.check_obj_collisions(self.collectible_obj_grid.get(tx_l, ty))
        self.check_obj_collisions(self.collectible_obj_grid.get(midpoint(tx_l, tx_r), ty))
        self.check_obj_collisions(self.collectible_obj_grid.get(tx_r, ty))

    def move_left(self):
        self.player.flip_horz = True
        new_rect = self.player.collide_rect.move(-Speed, 0)
        tx = int(new_rect.left / self.tmxdata.tilewidth)
        ty_t = int(new_rect.top / self.tmxdata.tileheight)
        ty_b = int(new_rect.bottom / self.tmxdata.tileheight)
        if not self.check_collide_tile(new_rect, tx, ty_t) and not self.check_collide_tile(new_rect, tx, ty_b):
            self.player.position = (new_rect.x, new_rect.y)

        # Check object collisions
        self.check_obj_collisions(self.collectible_obj_grid.get(tx, ty_t))
        self.check_obj_collisions(self.collectible_obj_grid.get(tx, midpoint(ty_t, ty_b)))
        self.check_obj_collisions(self.collectible_obj_grid.get(tx, ty_b))

    def move_right(self):
        self.player.flip_horz = False
        new_rect = self.player.collide_rect.move(Speed, 0)
        tx = int(new_rect.right / self.tmxdata.tilewidth)
        ty_t = int(new_rect.top / self.tmxdata.tileheight)
        ty_b = int(new_rect.bottom / self.tmxdata.tileheight)
        if not self.check_collide_tile(new_rect, tx, ty_t) and not self.check_collide_tile(new_rect, tx, ty_b):
            self.player.position = (new_rect.x, new_rect.y)

        # Check object collisions
        self.check_obj_collisions(self.collectible_obj_grid.get(tx, ty_t))
        self.check_obj_collisions(self.collectible_obj_grid.get(tx, midpoint(ty_t, ty_b)))
        self.check_obj_collisions(self.collectible_obj_grid.get(tx, ty_b))

    def update_game(self):
        self.keyboard.update()

        moved = False
        if self.keyboard.any_down([K_UP, K_DOWN, K_LEFT, K_RIGHT]):
            self.debug_rects.clear()

        if self.keyboard.down(K_UP):
            moved = True
            self.move_up()
        if self.keyboard.down(K_DOWN):
            moved = True
            self.move_down()
        if self.keyboard.down(K_LEFT):
            moved = True
            self.move_left()
        if self.keyboard.down(K_RIGHT):
            moved = True
            self.move_right()

        # Handle joystick input
        if self.joystick is not None:
            jx, jy = self.joystick.get_hat(0)
            if jy > 0:
                moved = True
                self.move_up()
            if jy < 0:
                moved = True
                self.move_down()
            if jx < 0:
                moved = True
                self.move_left()
            if jx > 0:
                moved = True
                self.move_right()

        if moved:
            self.player.curr_state_key = "walking"
        else:
            self.player.curr_state_key = "standing"

        if self.keyboard.down(K_RETURN):
            self.player_x = PlayerStartX
            self.player_y = PlayerStartY
        if self.keyboard.pressed(K_SPACE):
            obj_list = self.interaction_obj_grid.get_from_points([
                    self.player.rect.topleft,
                    self.player.rect.topright,
                    self.player.rect.bottomleft,
                    self.player.rect.bottomright
                ])
            
            for o in obj_list:
                logging.info("Interacted with {}".format(o))
                if o.type == "hint":
                    print("Hint: {}".format(o.properties["hint_text"]))

        if self.keyboard.down(K_ESCAPE):
            self.running = False

        for sp in self.group:
            sp.update(10)
        
    def check_collide_tile(self, player_rect, x, y):
        tile = self.get_main_tile(x, y)

        # Grab our tile properties, if any
        tile_props = self.tmxdata.tile_properties.get(tile, {})

        # If a tile in our set is marked as non-blocking, then don't collide.
        if tile_props.get("blocks", "all") == "none":
            return False

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


        self.group.center((self.player.rect.x, self.player.rect.y))
        #self.group.center((ScreenWidth/2, ScreenHeight/2))
        
        self.group.draw(self.off_screen)
        
        # Draw a solid blue circle in the center
        # pygame.draw.circle(self.off_screen, (0, 0, 255), (self.player_x, self.player_y), self.player_radius)
        # p_screen_pos = pygame.Rect(ScreenWidth/2, ScreenHeight/2, PlayerWidth, PlayerHeight)
        # pygame.draw.rect(self.off_screen, (0,0,255), p_screen_pos)

        #pygame.draw.rect(self.off_screen, (0,0,255), self.player.rect)

        map_offset = (self.player.rect.x-ScreenWidth/2, self.player.rect.y-ScreenHeight/2)
        for r in self.debug_rects:
            pygame.draw.rect(self.off_screen, (255,255,255), r.move((-map_offset[0], -map_offset[1])), width=1)

        txt = self.font.render("Score: " + str(self.score), False, pygame.Color('white'))
        self.off_screen.blit(txt, (5, 5))

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