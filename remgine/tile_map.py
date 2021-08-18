"""
A class using pytiled_parser and arcade to load/render tiled maps adding on
common actor movemnt/collision checks against map data.
"""

import itertools
import importlib

import arcade
# import pygame as pg
from .rect import Rect

import pytiled_parser
from pytiled_parser.objects import TileLayer

from remgine.object_grid import ObjectGrid

class TileMap:
    """
    The tile map holds the map data as well as object grids for various items.
    """

    #--------------------------------------------------------------------------
    def __init__(self, map_path, collision_layer_name):
        self.tmxdata = arcade.tilemap.read_tmx(map_path)

        # level_script = self.tmxdata.properties.get("start_script")
        # if level_script is not None:
        #     print("Got a level script from the level: " + level_script)
        #     level_module = importlib.import_module(level_script)
        #     level_module.start()

        self.collide_layer = arcade.tilemap.get_tilemap_layer(self.tmxdata, collision_layer_name)
        
        tile_layers = list(filter(lambda item: isinstance(item, TileLayer), self.tmxdata.layers))
        self.layer_sprites = []

        for tl in tile_layers:
            spr = arcade.process_layer(self.tmxdata, tl.name)
            self.layer_sprites.append(spr)

        # Create single dicctionary of tile properties
        tile_sets = list(self.tmxdata.tile_sets.values())
        self.tile_props = {}
        for tile_set in tile_sets:
            for tile_id in tile_set.tiles:
                if tile_id in self.tile_props:
                    raise RuntimeError(f"tile {tile_id} already in tile property map!")

                tile = tile_set.tiles[tile_id]
                self.tile_props[tile_id] = {}
                for p in tile.properties:
                    self.tile_props[tile_id][p.name] = p.value

        
        # self.map_data = pyscroll.TiledMapData(self.tmxdata)
        # self.main_tiles = self.tmxdata.get_layer_by_name(collision_layer_name)
        
        # buffered_renderer = pyscroll.BufferedRenderer(
        #         self.map_data, 
        #         (screen_width, screen_height), 
        #         clamp_camera=False
        #     )
        # self.group = pyscroll.PyscrollGroup(
        #         map_layer=buffered_renderer
        #     )
        self.obj_grids = {}
        self.type_to_obj_layers = {}
        self.type_to_obj_grids = {}

        # Look for an interactions property on the map.  We expect a set of 
        # lines with 'layer:game_type' to add to our list.
        interaction_property = self.tmxdata.properties.get("interaction", "")
        print(f"Got property: {interaction_property}")
        for line in interaction_property.splitlines():
            split = line.split(':')
            layer = split[0]
            obj_type = split[1]
            print(f"Adding layer {layer} for object type {obj_type}")
            layer_list = self.type_to_obj_layers.get(layer, [])
            layer_list.append(obj_type)
            self.type_to_obj_layers[layer] = layer_list

    #--------------------------------------------------------------------------
    def check_move_left(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        actor.flip_horz = True
        new_rect = actor.collide_rect.move(-amount, 0)
        new_rect.x += 1

        tys = range(
            int(new_rect.top / self.tmxdata.tile_size.height),
            int((new_rect.bottom + self.tmxdata.tile_size.height+1) / self.tmxdata.tile_size.height)
            )
        txs = itertools.repeat(int(new_rect.left / self.tmxdata.tile_size.width), len(tys))
        points = list(zip(txs, tys))

        # Check for tile collisions along line of interest
        hit = False
        for (tx, ty) in points:
            if self.check_collide_tile(new_rect, tx, ty):
                move_pos = ((tx+1)*self.tmxdata.tile_size.width + actor.collide_rect.w/2, actor.position[1])
                hit = True
                moved = False
                break
        
        # If we didn't hit any tile, then we can move.
        if not hit:
            move_pos = (actor.position[0]-amount, actor.position[1])
            moved = True

            # If we moved, check the registered object grid(s) for hits 
            self.check_obj_grid_collisions(actor, points)
            
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
        new_rect.x -= 1

        tys = range(
            int(new_rect.top / self.tmxdata.tile_size.height),
            int((new_rect.bottom + self.tmxdata.tile_size.height+1) / self.tmxdata.tile_size.height)
            )
        txs = itertools.repeat(int(new_rect.right / self.tmxdata.tile_size.width), len(tys))
        points = list(zip(txs, tys))

        # Check for tile collisions along line of interest
        hit = False
        for (tx, ty) in points:
            if self.check_collide_tile(new_rect, tx, ty):
                move_pos = ((tx)*self.tmxdata.tile_size.height - actor.collide_rect.w/2, actor.position[1])
                hit = True
                moved = False
                break
        
        # If we didn't hit any tile, then we can move.
        if not hit:
            move_pos = (actor.position[0]+amount, actor.position[1])
            moved = True

            # If we moved, check the registered object grid(s) for hits 
            self.check_obj_grid_collisions(actor, points)

        return (moved, move_pos)

    
    #--------------------------------------------------------------------------
    def check_move_down(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        # self.player_y = max(self.player_radius, self.player_y - Speed)
        new_rect = actor.collide_rect.move(0, -amount)
        new_rect.y -= 1
        txs = range(
            int(new_rect.left / self.tmxdata.tile_size.width),
            int((new_rect.right + self.tmxdata.tile_size.width+1) / self.tmxdata.tile_size.width)
            )
        tys = itertools.repeat(int(new_rect.top / self.tmxdata.tile_size.height), len(txs))
        points = list(zip(txs, tys))

        # Check for tile collisions along line of interest
        hit = False
        for (tx, ty) in points:
            if self.check_collide_tile(new_rect, tx, ty):
                move_pos = (actor.position[0], (ty+1)*self.tmxdata.tile_size.height)
                hit = True
                moved = False
                break
        
        # If we didn't hit any tile, then we can move.
        if not hit:
            move_pos = (actor.position[0], actor.position[1]-amount)
            moved = True
            
            # If we moved, check the registered object grid(s) for hits 
            self.check_obj_grid_collisions(actor, points)

        return (moved, move_pos)
    
    #--------------------------------------------------------------------------
    def check_move_up(self, actor, amount):
        """
        Checks if the actor could move left in the tile map.
        Returns (able_to_move, position_tuple)
        """
        moved = False
        new_rect = actor.collide_rect.move(0, amount)
        new_rect.y += 1
        txs = range(
            int(new_rect.left / self.tmxdata.tile_size.width),
            int((new_rect.right + self.tmxdata.tile_size.width+1) / self.tmxdata.tile_size.width)
            )
        tys = itertools.repeat(int(new_rect.bottom / self.tmxdata.tile_size.height), len(txs))
        points = list(zip(txs, tys))
        # Check for tile collisions along line of interest
        hit = False
        for (tx, ty) in points:
            if self.check_collide_tile(new_rect, tx, ty):
                move_pos = (actor.position[0], (ty)*self.tmxdata.tile_size.height -actor.collide_rect.h)
                hit = True
                moved = False
                break
        
        # If we didn't hit any tile, then we can move.
        if not hit:
            move_pos = (actor.position[0], actor.position[1] +amount)
            moved = True

            # If we moved, check the registered object grid(s) for hits 
            self.check_obj_grid_collisions(actor, points)
            
        return (moved, move_pos)

    def check_obj_grid_collisions(self, actor, points):
        if actor.game_type is None:
            return

        grids = self.type_to_obj_grids.get(actor.game_type, [])
        for (obj_grid, obj_context, hit_callback) in grids:
            for (tx, ty) in points:
                objs = obj_grid.get(tx, ty)
                if len(objs) > 0:
                    remaining = []
                    for o in objs:
                        if not hit_callback(obj_context, actor, o):
                            remaining.append(o)
                    obj_grid.set(tx, ty, remaining)

    #--------------------------------------------------------------------------
    def check_collide_tile(self, player_rect, x, y):
        tile = self.get_main_tile(x, y)

        # Grab our tile properties, if any
        # if tile == 0:
        #     return False
        # tile_props = self.tmxdata.tile_properties.get(tile, {})

        # # If a tile in our set is marked as non-blocking, then don't collide.
        if tile != 0:
            if self.tile_props.get(tile-1, {}).get("blocks", "all") == "none":
                return False

            tw = self.tmxdata.tile_size.width
            th = self.tmxdata.tile_size.height

            collide_rect = Rect(int(x*tw), int(y*th), tw, th)
            # TODO: Add debug rect back in
            # Debug, draw collide rect.
            # self.debug_rects.append(collide_rect)

            return player_rect.colliderect(collide_rect)
        else:
            return False

    #--------------------------------------------------------------------------
    def get_main_tile(self, x, y):
        y_height = len(self.collide_layer.layer_data)
        return self.collide_layer.layer_data[int(y_height-y)][int(x)]

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
                self.tmxdata.tile_size.width, 
                self.tmxdata.tile_size.height
            )
        obj_group = self.tmxdata.get_layer_by_name(layer_name)
        for obj in self.type_to_obj_layers[layer_name]:
            obj_grid_list = self.type_to_obj_grids.get(obj, [])
            obj_grid_list.append((obj_grid, context, hit_callback))
            self.type_to_obj_grids[obj] = obj_grid_list

        for obj in obj_group:
            # print(f"Inserting object {obj.type} at {obj.x}, {obj.y} with name '{obj.name}', from {layer_name}")
            sprite = create_callback(context, obj)
            if sprite is not None:
                obj.sprite = sprite
                self.group.add(obj.sprite)
            obj_grid.insert_obj((obj.x, obj.y, obj.width, obj.height), obj)
        self.obj_grids[layer_name] = (obj_grid, context, hit_callback)
        return obj_grid

    def draw(self):
        for layer in self.layer_sprites:
            layer.draw()
            # self.collide_layer_sprites.draw()