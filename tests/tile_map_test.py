import os
import sys

import pytest
import arcade
import pytiled_parser

from pytiled_parser.objects import TileLayer

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_ROOT, "..", "assets")

sys.path.append(os.path.join(SCRIPT_ROOT, ".."))
from remgine import tile_map

def test_can_read_map_properties():
    # Read in the tiled map
    my_map = arcade.tilemap.read_tmx(os.path.join(ASSETS_DIR, "level1.tmx"))

    # Check for map properties
    assert my_map.properties["player_start_x"] == '3'
    assert my_map.properties["player_start_y"] == '4'
    assert my_map.properties["start_script"] == "assets.scripts.level1"

def test_can_tile_properties():
    # Read in the tiled map
    my_map = arcade.tilemap.read_tmx(os.path.join(ASSETS_DIR, "level1.tmx"))

    # Check for tile properties
    tile_sets = list(my_map.tile_sets.values())
    tile_set = tile_sets[0]
    tile1 = tile_set.tiles[0]

    assert tile1.properties[0].name == "blocks"
    assert tile1.properties[0].value == "none"

def test_can_create_dict_of_tile_props():
    my_map = arcade.tilemap.read_tmx(os.path.join(ASSETS_DIR, "level1.tmx"))
    tile_sets = list(my_map.tile_sets.values())
    tile_props = {}
    for tile_set in tile_sets:
        for tile_id in tile_set.tiles:
            if tile_id in tile_props:
                raise RuntimeError(f"tile {k} already in tile property map!")

            tile = tile_set.tiles[tile_id]
            tile_props[tile_id] = {}
            for p in tile.properties:
                tile_props[tile_id][p.name] = p.value
    
    assert tile_props[1]["blocks"] == "none"

def test_can_read_map_data():
    # Read in the tiled map
    my_map = arcade.tilemap.read_tmx(os.path.join(ASSETS_DIR, "level1.tmx"))

    l = arcade.tilemap.get_tilemap_layer(my_map, "main_layer")

    # Check the first few tiles are what we expect
    assert l.layer_data[0][0] == 100 # left wall
    assert l.layer_data[0][1] == 0  # empty
    assert l.layer_data[0][2] == 63 # tree top
    
    # Check another line is also what we expect.
    assert l.layer_data[7][0] == 100 # left wall
    assert l.layer_data[7][1] == 3   # grass tile
    assert l.layer_data[7][2] == 3   # grass tile

def test_can_read_object_data():
    # Read in the tiled map
    my_map = arcade.tilemap.read_tmx(os.path.join(ASSETS_DIR, "level1.tmx"))

    l = arcade.tilemap.get_tilemap_layer(my_map, "collidable_objects")

    assert isinstance(l, pytiled_parser.objects.ObjectLayer)

    assert len(l.tiled_objects) == 6

    # Note, objects are stored in id order, which was descending in map editor.
    assert l.tiled_objects[5].name == "checkpoint_2"
    assert l.tiled_objects[4].name == "checkpoint_1a"

    assert l.tiled_objects[3].name == "change_to_level_2"
    assert l.tiled_objects[3].type == "changeLevel"
    assert l.tiled_objects[3].properties["level_name"] == "Content/level2.tmx"
    
    assert l.tiled_objects[2].name == "secret_sound"
    assert l.tiled_objects[2].type == "run_script"
    assert l.tiled_objects[2].properties["script"] == "Content/play_secret_cue.lua"

    assert l.tiled_objects[1].name == "checkpoint_1b"
    assert l.tiled_objects[0].name == "checkpoint_3"

def test_can_list_all_layers():
    # Read in the tiled map
    my_map = arcade.tilemap.read_tmx(os.path.join(ASSETS_DIR, "level1.tmx"))
    layers = my_map.layers

    # Check the tile layers only
    tile_layers = list(filter(lambda item: isinstance(item, TileLayer), layers))

    assert len(tile_layers) == 4
    assert layers[0].name == "background_tiles"
    assert layers[1].name == "main_layer"
    assert layers[2].name == "object layer" # Old layer, shoul dbe removed.
    assert layers[3].name == "foreground_tiles"