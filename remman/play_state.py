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

def game_obj_create_cb(_context, obj):
    if obj.type == "dot":
        print("Adding dot.")
        sprite = remgine.Actor({"normal": DotFrames}, "normal", (obj.x, obj.y))
        
    elif obj.type == "power_dot":
        print("Adding power dot.")
        sprite = remgine.Actor({"normal": PowerDotFrames}, "normal", (obj.x, obj.y))
        
    elif obj.type == "ghost":
        sprite = RedGhost( 
            (obj.x, obj.y)
        )
    return sprite

class Player(remgine.Actor):
    def __init__(self):
        remgine.Actor.__init__(self, {
            "right": MsPacManFrames
        }, "right")
        self.collide_adjust = (0, 0, 8, 8)
        self.scale = 0.8
        self.gravity = (8, 12)
        self.direction = Direction.Stopped
        self.next_direction = Direction.Stopped
        self.position = (8, 8)

    def update(self, time_elapsed_ms, context):
        kb = context.context.keyboard

        if kb.down(K_UP):
            self.next_direction = Direction.Up
            
        if self.direction == Direction.Up or self.next_direction == Direction.Up:
            (moved, self.position) = context.map.check_move_up(self, Speed)
            if moved:
                self.direction = Direction.Up

        if kb.down(K_DOWN):
            self.next_direction = Direction.Down
            
        if self.direction == Direction.Down or self.next_direction == Direction.Down:
            (moved, self.position) = context.map.check_move_down(self, Speed)
            if moved:
                self.direction = Direction.Down

        if kb.down(K_LEFT):
            self.next_direction = Direction.Left
            
        if self.direction == Direction.Left or self.next_direction == Direction.Left:
            (moved, self.position) = context.map.check_move_left(self, Speed)
            if moved:
                self.direction = Direction.Left

        if kb.down(K_RIGHT):
            self.next_direction = Direction.Right
            
        if self.direction == Direction.Right or self.next_direction == Direction.Right:
            (moved, self.position) = context.map.check_move_right(self, Speed)
            if moved:
                self.direction = Direction.Right

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
        
        remgine.Actor.update(self, time_elapsed_ms, context)


DirCheckTime = 2000
class RedGhost(remgine.Actor):
    def __init__(self, position=(0,0)):
        remgine.Actor.__init__(self, {
                "right": RedGhostRightFrames,
                "up": RedGhostUpFrames,
                "down": RedGhostDownFrames
            }, 
            "right", 
            position
        )
        self.collide_adjust = (0, 0, 8, 8)
        self.dir_check_time = 0
        self.direction = Direction.Stopped

    def update(self, time_elapsed_ms, context):
        remgine.Actor.update(self, time_elapsed_ms, context)
        self.dir_check_time -= time_elapsed_ms
        if self.dir_check_time < 0:
            self.dir_check_time = DirCheckTime
            self.direction = random.choice([Direction.Up, Direction.Down, Direction.Left, Direction.Right])
        else:
            if self.direction == Direction.Up:
                (_moved, self.position) = context.map.check_move_up(self, Speed)
            elif self.direction == Direction.Down:
                (_moved, self.position) = context.map.check_move_down(self, Speed)
            elif self.direction == Direction.Left:
                (_moved, self.position) = context.map.check_move_left(self, Speed)
            elif self.direction == Direction.Right:
                (_moved, self.position) = context.map.check_move_right(self, Speed)

class PlayState(remgine.GameState):
    def __init__(self, context):
        remgine.GameState.__init__(self, context)
        
        self.font = pg.font.Font(None, 15)
        self.running = True
        self.score = 0
        
        self.player = Player()

        self.map = remgine.TileMap(
                "assets/level1.tmx", 
                "main_layer", 
                ScreenWidth, 
                ScreenHeight)

        # level_script = self.tmxdata.properties.get("start_script")
        # if level_script is not None:
        #     print("Got a level script from the level: " + level_script)
        #     level_module = importlib.import_module(level_script)
        #     level_module.start()

        self.map.group.add(self.player)

        # Create an object grid and register our map objects into it.
        self.collectible_obj_grid = self.map.create_obj_grid(
                "dots", 
                game_obj_create_cb,
                PlayState.handle_obj_collide,
                self
            )

        # if pygame.joystick.get_count() > 0:
        #     self.joystick = joystick = pygame.joystick.Joystick(0)
        #     self.joystick.init()
        # else:
        #     self.joystick = None
        self.debug_rects = []

    def handle_obj_collide(self, _actor, o):
        print(f"Hit object: '{o.type}'")
        if o.type == "dot" and o.sprite in self.map.group:
            self.score += 100
            self.map.group.remove(o.sprite)
            return True
        if o.type == "power_dot" and o.sprite in self.map.group:
            self.score += 500
            self.map.group.remove(o.sprite)
            return True
        if o.name == "ghost" and o.sprite in self.map.group:
            if o.sprite.curr_state_key != "killed":
                o.sprite.curr_state_key = "killed"            
        return False

    def update(self):
        
        kb = self.context.keyboard

        if kb.any_down([K_UP, K_DOWN, K_LEFT, K_RIGHT]):
            self.debug_rects.clear()

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
        # self.group.center((self.player.rect.x, self.player.rect.y))
        #self.group.center((ScreenWidth/2, ScreenHeight/2))
        
        self.map.group.draw(self.context.off_screen)

        map_offset = (0,0)#(self.player.rect.x-ScreenWidth/2, self.player.rect.y-ScreenHeight/2)
        for r in self.debug_rects:
            pg.draw.rect(self.context.off_screen, (255,255,255), r.move((-map_offset[0], -map_offset[1])), width=1)

        # txt = self.font.render("Score: " + str(self.score), False, pygame.Color('white'))
        # self.off_screen.blit(txt, (5, 5))
