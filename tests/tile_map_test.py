import os

import pytest
import arcade

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

