import os

import pytest
import arcade

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_ROOT, "..", "assets")

def test_can_read_map_data():
    # Read in the tiled map
    my_map = arcade.tilemap.read_tmx(os.path.join(ASSETS_DIR, "level1.tmx"))

    # Check for map properties
    assert my_map.properties["player_start_x"] == 3
    assert my_map.properties["player_start_y"] == 4
    assert my_map.properties["start_script"] == "assets.scripts.level1"
