# Rem-man - the game.
import math
import random
import importlib
import logging
from remman.constants import Direction, ScreenWidth
import sys


import pygame as pg
from pygame.locals import *

from constants import *

import pytmx
from pytmx.util_pygame import load_pygame
import pyscroll

import remgine

def midpoint(a, b):
        return int(a + (b-a)/2)

class PlayState(remgine.GameState):
    def __init__(self, context):
        remgine.GameState.__init__(self, context)
        
        self.font = pg.font.Font(None, 15)
        self.running = True
        self.score = 0
        
        self.player = remgine.Actor({
            "right": MsPacManFrames
        }, "right")

        self.player.collide_adjust = (0, 0, 8, 8)
        self.player.scale = 0.8
        self.player.gravity = (8, 12)
        self.player.direction = Direction.Stopped
        self.player.next_direction = Direction.Stopped
        self.player.position = (8, 8)

        self.map = remgine.TileMap(
                "assets/level1.tmx", 
                "main_layer", 
                ScreenWidth, 
                ScreenHeight)

        # self.tmxdata = load_pygame("assets/level1.tmx")

        # level_script = self.tmxdata.properties.get("start_script")
        # if level_script is not None:
        #     print("Got a level script from the level: " + level_script)
        #     level_module = importlib.import_module(level_script)
        #     level_module.start()

        # self.map_data = pyscroll.TiledMapData(self.tmxdata)
        # self.main_tiles = self.tmxdata.get_layer_by_name("main_layer")
        
        # self.map_layer = pyscroll.BufferedRenderer(self.map_data, (ScreenWidth, ScreenHeight), clamp_camera=False)
        # self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        self.map.group.add(self.player)

        # Create an object grid and register our map objects into it.
        # self.collectible_obj_grid = self.create_obj_grid("dots")


        # self.interaction_obj_grid = self.create_obj_grid("interaction_objects")
        
        # if pygame.joystick.get_count() > 0:
        #     self.joystick = joystick = pygame.joystick.Joystick(0)
        #     self.joystick.init()
        # else:
        #     self.joystick = None
        self.debug_rects = []

    def create_obj_grid(self, layer_name):
        obj_grid = remgine.ObjectGrid(self.tmxdata.width, self.tmxdata.height, self.tmxdata.tilewidth, self.tmxdata.tileheight)
        obj_group = self.tmxdata.get_layer_by_name(layer_name)
        for obj in obj_group:
            print(f"Inserting object {obj.type} at {obj.x}, {obj.y} with name '{obj.name}', from {layer_name}")
            if obj.type == "dot":
                print("Adding dot.")
                obj.sprite = remgine.Actor({"normal": DotFrames}, "normal", (obj.x, obj.y))
                obj.sprite.scale = 1
                self.group.add(obj.sprite)
            elif obj.type == "power_dot":
                print("Adding power dot.")
                obj.sprite = remgine.Actor({"normal": PowerDotFrames}, "normal", (obj.x, obj.y))
                obj.sprite.scale = 1
                self.group.add(obj.sprite)
            elif obj.name == "ghost":
                obj.sprite = remgine.Actor({
                        "walking": self.GoombaWalk,
                        "killed": self.GoombaDie
                    }, 
                    "walking", 
                    (obj.x, obj.y)
                )
                self.group.add(obj.sprite)

            obj_grid.insert_obj((obj.x, obj.y, obj.width, obj.height), obj)

        return obj_grid

    def check_obj_collisions(self, tx, ty):
        objs = self.collectible_obj_grid.get(tx, ty)
        if len(objs) > 0:
            for o in objs:
                print(f"Hit object: '{o.type}'")
                if o.type == "dot" and o.sprite in self.group:
                    self.score += 100
                    self.group.remove(o.sprite)
                    objs.remove(o)
                if o.type == "power_dot" and o.sprite in self.group:
                    self.score += 500
                    self.group.remove(o.sprite)
                    objs.remove(o)
                if o.name == "ghost" and o.sprite in self.group:
                    if o.sprite.curr_state_key != "killed":
                        o.sprite.curr_state_key = "killed"

    def move_up(self, amount = -Speed):
        return self.map.check_move_up(self.player, amount)

        # Check object collisions
        # self.check_obj_collisions(tx_l, ty)
        # self.check_obj_collisions(midpoint(tx_l, tx_r), ty)
        # self.check_obj_collisions(tx_r, ty)
        # return moved
        
    def move_down(self, amount = Speed):
        return self.map.check_move_down(self.player, amount)
        
        # Check object collisions
        # self.check_obj_collisions(tx_l, ty)
        # self.check_obj_collisions(midpoint(tx_l, tx_r), ty)
        # self.check_obj_collisions(tx_r, ty)
        # return moved

    def move_left(self, amount = Speed):
        return self.map.check_move_left(self.player, amount)
        # Check object collisions
        # self.check_obj_collisions(tx, ty_t)
        # self.check_obj_collisions(tx, midpoint(ty_t, ty_b))
        # self.check_obj_collisions(tx, ty_b)
        # return moved

    def move_right(self, amount = Speed):
        return self.map.check_move_right(self.player, amount)
        
        # Check object collisions
        # self.check_obj_collisions(tx, ty_t)
        # self.check_obj_collisions(tx, midpoint(ty_t, ty_b))
        # self.check_obj_collisions(tx, ty_b)
        # return moved

    def update(self):
        kb = self.context.keyboard

        if kb.any_down([K_UP, K_DOWN, K_LEFT, K_RIGHT]):
            self.debug_rects.clear()

        if kb.down(K_UP):
            self.player.next_direction = Direction.Up
            
        if self.player.direction == Direction.Up or self.player.next_direction == Direction.Up:
            (moved, self.player.position) = self.move_up()
            if moved:
                self.player.direction = Direction.Up

        if kb.down(K_DOWN):
            self.player.next_direction = Direction.Down
            
        if self.player.direction == Direction.Down or self.player.next_direction == Direction.Down:
            (moved, self.player.position) = self.move_down()
            if moved:
                self.player.direction = Direction.Down

        if kb.down(K_LEFT):
            self.player.next_direction = Direction.Left
            
        if self.player.direction == Direction.Left or self.player.next_direction == Direction.Left:
            (moved, self.player.position) = self.move_left()
            if moved:
                self.player.direction = Direction.Left

        if kb.down(K_RIGHT):
            self.player.next_direction = Direction.Right
            
        if self.player.direction == Direction.Right or self.player.next_direction == Direction.Right:
            (moved, self.player.position) = self.move_right()
            if moved:
                self.player.direction = Direction.Right

        # Handle joystick input
        # if self.joystick is not None:
        #     jx, jy = self.joystick.get_hat(0)
        #     if jy > 0:
        #         moved = True
        #         self.move_up()
        #     if jy < 0:
        #         moved = True
        #         self.move_down()
        #     if jx < 0:
        #         moved = True
        #         self.move_left()
        #     if jx > 0:
        #         moved = True
        #         self.move_right()

        # if moved:
        #     self.player.curr_state_key = "walking"
        # else:
        #     self.player.curr_state_key = "standing"

        # if kb.pressed(K_SPACE):
        #     obj_list = self.interaction_obj_grid.get_from_points([
        #             self.player.rect.topleft,
        #             self.player.rect.topright,
        #             self.player.rect.bottomleft,
        #             self.player.rect.bottomright
        #         ])
            
        #     for o in obj_list:
        #         logging.info("Interacted with {}".format(o))
        #         if o.type == "hint":
        #             print(f"Hint: {o.properties['hint_text']}")

        if kb.down(K_ESCAPE):
            self.running = False

        for sp in self.map.group:
            sp.update(10, self)
        
    

    def render(self):
        # Fill the background with white
        # self.off_screen.fill((0,0,0))


        # self.group.center((self.player.rect.x, self.player.rect.y))
        #self.group.center((ScreenWidth/2, ScreenHeight/2))
        
        self.map.group.draw(self.context.off_screen)
        
        # Draw a solid blue circle in the center
        # pygame.draw.circle(self.off_screen, (0, 0, 255), (self.player_x, self.player_y), self.player_radius)
        # p_screen_pos = pygame.Rect(ScreenWidth/2, ScreenHeight/2, PlayerWidth, PlayerHeight)
        # pygame.draw.rect(self.off_screen, (0,0,255), p_screen_pos)

        #pygame.draw.rect(self.off_screen, (0,0,255), self.player.rect)

        map_offset = (0,0)#(self.player.rect.x-ScreenWidth/2, self.player.rect.y-ScreenHeight/2)
        for r in self.debug_rects:
            pg.draw.rect(self.context.off_screen, (255,255,255), r.move((-map_offset[0], -map_offset[1])), width=1)

        # txt = self.font.render("Score: " + str(self.score), False, pygame.Color('white'))
        # self.off_screen.blit(txt, (5, 5))

        # self.screen.blit(pg.transform.scale(self.off_screen, self.screen.get_rect().size), (0, 0))
        # Flip the display
        # pygame.display.flip()
