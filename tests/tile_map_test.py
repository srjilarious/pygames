import os

import pytest
import arcade
import pytiled_parser

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_ROOT, "..", "assets")

def test_can_read_map_properties():
    # Read in the tiled map
    my_map = arcade.tilemap.read_tmx(os.path.join(ASSETS_DIR, "level1.tmx"))

    # Check for map properties
    assert my_map.properties["player_start_x"] == '3'
    assert my_map.properties["player_start_y"] == '4'
    assert my_map.properties["start_script"] == "assets.scripts.level1"

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
