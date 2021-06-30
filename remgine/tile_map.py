"""
A class using pytile and pyscroll to load/render tileed maps adding on
common actor movemnt/collision checks against map data.
"""

import itertools
import pygame as pg
import pytmx
from pytmx.util_pygame import load_pygame
import pyscroll
import importlib
from remgine.object_grid import ObjectGrid

class TileMap:
    """
    The tile map holds the map data as well as object grids for various items.
    """

    #--------------------------------------------------------------------------
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
        self.obj_grids = {}

    #--------------------------------------------------------------------------
    def check_move_left(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        actor.flip_horz = True
        new_rect = actor.collide_rect.move(-amount, 0)
        new_rect.left -= 1

        tys = range(
            int(new_rect.top / self.tmxdata.tileheight),
            int((new_rect.bottom + self.tmxdata.tileheight+1) / self.tmxdata.tileheight)
            )
        txs = itertools.repeat(int(new_rect.left / self.tmxdata.tilewidth), len(tys))
        points = list(zip(txs, tys))

        # Check for tile collisions along line of interest
        hit = False
        for (tx, ty) in points:
            if self.check_collide_tile(new_rect, tx, ty):
                move_pos = ((tx+1)*self.tmxdata.tileheight, actor.position[1])
                hit = True
                moved = False
                break
        
        # If we didn't hit any tile, then we can move.
        if not hit:
            move_pos = (actor.position[0]-amount, actor.position[1])
            moved = True

            # If we moved, we can check the registered object grid(s) for
            # hits 
            for (obj_grid, obj_context, hit_callback) in self.obj_grids.values():
                for (tx, ty) in points:
                    objs = obj_grid.get(tx, ty)
                    if len(objs) > 0:
                        remaining = []
                        for o in objs:
                            if not hit_callback(obj_context, actor, o):
                                remaining.append(o)
                        obj_grid.set(tx, ty, remaining)
        return (moved, move_pos)
    
    #--------------------------------------------------------------------------
    def check_move_right(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        actor.flip_horz = False
        new_rect = actor.collide_rect.move(amount, 0)
        new_rect.right += 1

        tys = range(
            int(new_rect.top / self.tmxdata.tileheight),
            int((new_rect.bottom + self.tmxdata.tileheight+1) / self.tmxdata.tileheight)
            )
        txs = itertools.repeat(int(new_rect.right / self.tmxdata.tilewidth), len(tys))
        points = list(zip(txs, tys))

        # Check for tile collisions along line of interest
        hit = False
        for (tx, ty) in points:
            if self.check_collide_tile(new_rect, tx, ty):
                move_pos = ((tx)*self.tmxdata.tileheight - actor.collide_rect[2], actor.position[1])
                hit = True
                moved = False
                break
        
        # If we didn't hit any tile, then we can move.
        if not hit:
            move_pos = (actor.position[0]+amount, actor.position[1])
            moved = True

            # If we moved, we can check the registered object grid(s) for
            # hits 
            for (obj_grid, obj_context, hit_callback) in self.obj_grids.values():
                for (tx, ty) in points:
                    objs = obj_grid.get(tx, ty)
                    if len(objs) > 0:
                        remaining = []
                        for o in objs:
                            if not hit_callback(obj_context, actor, o):
                                remaining.append(o)
                        obj_grid.set(tx, ty, remaining)
        return (moved, move_pos)

    
    #--------------------------------------------------------------------------
    def check_move_up(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        # self.player_y = max(self.player_radius, self.player_y - Speed)
        new_rect = actor.collide_rect.move(0, -amount)
        new_rect.top -= 1
        txs = range(
            int(new_rect.left / self.tmxdata.tilewidth),
            int((new_rect.right + self.tmxdata.tilewidth+1) / self.tmxdata.tilewidth)
            )
        tys = itertools.repeat(int(new_rect.top / self.tmxdata.tileheight), len(txs))
        points = list(zip(txs, tys))

        # Check for tile collisions along line of interest
        hit = False
        for (tx, ty) in points:
            if self.check_collide_tile(new_rect, tx, ty):
                move_pos = (actor.position[0], (ty+1)*self.tmxdata.tileheight)
                hit = True
                moved = False
                break
        
        # If we didn't hit any tile, then we can move.
        if not hit:
            move_pos = (actor.position[0], actor.position[1]-amount)
            moved = True
            
            # If we moved, we can check the registered object grid(s) for
            # hits 
            for (obj_grid, obj_context, hit_callback) in self.obj_grids.values():
                for (tx, ty) in points:
                    objs = obj_grid.get(tx, ty)
                    if len(objs) > 0:
                        remaining = []
                        for o in objs:
                            if not hit_callback(obj_context, actor, o):
                                remaining.append(o)
                        obj_grid.set(tx, ty, remaining)

        return (moved, move_pos)
    
    #--------------------------------------------------------------------------
    def check_move_down(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        new_rect = actor.collide_rect.move(0, amount)
        new_rect.bottom += 1
        txs = range(
            int(new_rect.left / self.tmxdata.tilewidth),
            int((new_rect.right + self.tmxdata.tilewidth+1) / self.tmxdata.tilewidth)
            )
        tys = itertools.repeat(int(new_rect.bottom / self.tmxdata.tileheight), len(txs))
        points = list(zip(txs, tys))
        # Check for tile collisions along line of interest
        hit = False
        for (tx, ty) in points:
            if self.check_collide_tile(new_rect, tx, ty):
                move_pos = (actor.position[0], (ty)*self.tmxdata.tileheight -actor.collide_rect[3])
                hit = True
                moved = False
                break
        
        # If we didn't hit any tile, then we can move.
        if not hit:
            move_pos = (actor.position[0], actor.position[1] +amount)
            moved = True

            # If we moved, we can check the registered object grid(s) for
            # hits 
            for (obj_grid, obj_context, hit_callback) in self.obj_grids.values():
                for (tx, ty) in points:
                    objs = obj_grid.get(tx, ty)
                    if len(objs) > 0:
                        remaining = []
                        for o in objs:
                            if not hit_callback(obj_context, actor, o):
                                remaining.append(o)
                        obj_grid.set(tx, ty, remaining)
            
        return (moved, move_pos)

    #--------------------------------------------------------------------------
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

    #--------------------------------------------------------------------------
    def get_main_tile(self, x, y):
        return self.main_tiles.data[int(y)][int(x)]

    #--------------------------------------------------------------------------
    def create_obj_grid(self, layer_name, create_callback, hit_callback, context):
        """
        Creates an object grid for tile aligned objects from a layer.
        layer_name: The layer from the tile map to iterate over
        create_callback: A function that handles creating a sprite type object given the context, and the object reference.
        hit_callback: A callback to call when checking actor movement within map. Callback receives (context, actor, object) and should return true if object should be removed from grid,
        obj_context: the context to be passed to the hit callback.
        """
        obj_grid = ObjectGrid(
                self.tmxdata.width, 
                self.tmxdata.height, 
                self.tmxdata.tilewidth, 
                self.tmxdata.tileheight
            )
        obj_group = self.tmxdata.get_layer_by_name(layer_name)

        for obj in obj_group:
            # print(f"Inserting object {obj.type} at {obj.x}, {obj.y} with name '{obj.name}', from {layer_name}")
            sprite = create_callback(context, obj)
            if sprite is not None:
                obj.sprite = sprite
                self.group.add(obj.sprite)
            obj_grid.insert_obj((obj.x, obj.y, obj.width, obj.height), obj)
        self.obj_grids[layer_name] = (obj_grid, context, hit_callback)
        return obj_grid
