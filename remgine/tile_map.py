"""
A class using pytile and pyscroll to load/render tileed maps adding on
common actor movemnt/collision checks against map data.
"""

import pygame as pg
import pytmx
from pytmx.util_pygame import load_pygame
import pyscroll
import importlib

class TileMap:
    """
    The tile map holds the map data as well as object grids for various items.
    """
    def __init__(self, map_path, collision_layer_name, screen_width, screen_height):
        self.tmxdata = load_pygame(map_path)

        # level_script = self.tmxdata.properties.get("start_script")
        # if level_script is not None:
        #     print("Got a level script from the level: " + level_script)
        #     level_module = importlib.import_module(level_script)
        #     level_module.start()

        self.map_data = pyscroll.TiledMapData(self.tmxdata)
        self.main_tiles = self.tmxdata.get_layer_by_name(collision_layer_name)
        
        buffered_renderer = pyscroll.BufferedRenderer(
                self.map_data, 
                (screen_width, screen_height), 
                clamp_camera=False
            )
        self.group = pyscroll.PyscrollGroup(
                map_layer=buffered_renderer
            )

    def check_move_left(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        actor.flip_horz = True
        new_rect = actor.collide_rect.move(-amount, 0)
        new_rect.left -= 1
        tx = int(new_rect.left / self.tmxdata.tilewidth)
        ty_t = int(new_rect.top / self.tmxdata.tileheight)
        ty_b = int(new_rect.bottom / self.tmxdata.tileheight)
        if not self.check_collide_tile(new_rect, tx, ty_t) and not self.check_collide_tile(new_rect, tx, ty_b):
            move_pos = (actor.position[0]-amount, actor.position[1])
            moved = True
        else:
            move_pos = ((tx+1)*self.tmxdata.tileheight, actor.position[1])
        
        return (moved, move_pos)
    
    def check_move_right(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        actor.flip_horz = False
        new_rect = actor.collide_rect.move(amount, 0)
        new_rect.right += 1
        tx = int(new_rect.right / self.tmxdata.tilewidth)
        ty_t = int(new_rect.top / self.tmxdata.tileheight)
        ty_b = int(new_rect.bottom / self.tmxdata.tileheight)
        if not self.check_collide_tile(new_rect, tx, ty_t) and not self.check_collide_tile(new_rect, tx, ty_b):
            # self.player.position = (new_rect.x, new_rect.y)
            move_pos = (actor.position[0]+amount, actor.position[1])
            moved = True
        else:
            move_pos = ((tx)*self.tmxdata.tileheight - actor.collide_rect[2], actor.position[1])
        return (moved, move_pos)

    
    def check_move_up(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        # self.player_y = max(self.player_radius, self.player_y - Speed)
        new_rect = actor.collide_rect.move(0, amount)
        new_rect.top -= 1
        ty = int(new_rect.top / self.tmxdata.tileheight)
        tx_l = int(new_rect.left / self.tmxdata.tilewidth)
        tx_r = int(new_rect.right / self.tmxdata.tilewidth)
        if not self.check_collide_tile(new_rect, tx_l, ty) and not self.check_collide_tile(new_rect, tx_r, ty):
            move_pos = (actor.position[0], actor.position[1] +amount)
            moved = True
        else:
            move_pos = (actor.position[0], (ty+1)*self.tmxdata.tileheight)
        return (moved, move_pos)
    
    def check_move_down(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        new_rect = actor.collide_rect.move(0, amount)
        new_rect.bottom += 1
        ty = int(new_rect.bottom / self.tmxdata.tileheight)
        tx_l = int(new_rect.left / self.tmxdata.tilewidth)
        tx_r = int(new_rect.right / self.tmxdata.tilewidth)
        if not self.check_collide_tile(new_rect, tx_l, ty) and not self.check_collide_tile(new_rect, tx_r, ty):
            move_pos = (actor.position[0], actor.position[1] +amount)
            moved = True
        else:
            move_pos = (actor.position[0], (ty)*self.tmxdata.tileheight -actor.collide_rect[3])
        return (moved, move_pos)

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
            collide_rect = pg.Rect(int(x*tw), int(y*th), tw, th)
            # TODO: Add debug rect back in
            # Debug, draw collide rect.
            # self.debug_rects.append(collide_rect)

            return player_rect.colliderect(collide_rect)
        else:
            return False

    def get_main_tile(self, x, y):
        return self.main_tiles.data[int(y)][int(x)]