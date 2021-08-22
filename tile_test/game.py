# Tile engine pygame test
import math
import random
import importlib
import logging
import sys
import re

import arcade
import arcade.key as key

sys.path.append("..")
import remgine
import remgine.console

WindowWidth = 1280
WindowHeight = 720
ScreenWidth = 640
ScreenHeight = 360
PlayerStartX = 64
PlayerStartY = 64
PlayerWidth = 32
PlayerHeight = 32
Speed = 2


# BluePiece = pygame.image.load("blue_piece.png")
SpriteSheet = "../assets/game_content5.png"

def midpoint(a, b):
        return int(a + (b-a)/2)

class Player(remgine.Actor):
    def __init__(self):
        super().__init__({
            "standing": remgine.Frames(SpriteSheet, 
            [ 
                remgine.Frame(400, (557, 0, 42, 65)),
                remgine.Frame(400, (557, 68, 42, 65), (1, 0), (-1, 0)),
            ], allows_flip_horz=True),
            "walking": remgine.Frames(SpriteSheet, 
            [ 
                remgine.Frame(100, (368, 296, 50, 65)),
                remgine.Frame(100, (302, 358, 50, 65)),
                remgine.Frame(100, (420, 256, 50, 65)),
                remgine.Frame(100, (354, 363, 50, 65)),
                remgine.Frame(100, (420, 323, 50, 65)),
                remgine.Frame(100, (406, 390, 50, 65)),
                remgine.Frame(100, (458, 390, 50, 65)),
                remgine.Frame(100, (505, 0, 50, 65)),
            ], allows_flip_horz=True),
            "hit": remgine.Frames(SpriteSheet, 
            [ 
                remgine.Frame(60, (0, 0, 98, 91), (4, 24), (38, 24)),
                remgine.Frame(60, (98, 0, 98, 91), (4, 24), (38, 24)),
                remgine.Frame(60, (0, 91, 98, 91), (4, 24), (38, 24)),
                remgine.Frame(60, (98, 91, 98, 91), (4, 24), (38, 24)),
                remgine.Frame(60, (196, 0, 98, 91), (4, 24), (38, 24)),
                remgine.Frame(60, (196, 91, 98, 91), (4, 24), (38, 24)),
                remgine.Frame(60, (294, 0, 98, 91), (4, 24), (38, 24)),
                remgine.Frame(60, (294, 91, 98, 91), (4, 24), (38, 24)),
            ], allows_flip_horz=True, next_state="standing", play_type=remgine.PlayType.Once)
        }, "walking")

        self.position = (280,150)
        self.collide_adjust = (0, 0, 40, 60)
        self.jumping = False
        self.vel_y = 0

    def update(self, delta_time, context, map, camera):
        kb = context.keyboard

        moved_horz = False
        moved_vert = False
        tried_move = False
            
        if kb.down(key.LEFT):
            tried_move = True
            (moved_horz, self.position) = map.check_move_left(self, 4)
        if kb.down(key.RIGHT):
            tried_move = True
            (moved_horz, self.position) = map.check_move_right(self, 4)

        if kb.down(key.UP) and not self.jumping:
            tried_move = True
            self.jumping = True
            self.vel_y = 12

        if self.vel_y > -7:
            self.vel_y -= 0.3

        if self.vel_y > 0:
            (moved_vert, self.position) = map.check_move_up(self, int(self.vel_y))
            if not moved_vert:
                self.vel_y = 0
        else:
            (moved_vert, self.position) = map.check_move_down(self, int(-self.vel_y))
            if not moved_vert:
                self.jumping = False
            else:
                self.jumping = True
            
        if moved_horz or moved_vert:
            camera.goal_x = int(self.position[0] - context.screen_size[0]/2)
            camera.goal_y = int(self.position[1] - context.screen_size[1]/2)
        
        if tried_move:
            self.curr_state_key = "walking"
        else:
            self.curr_state_key = "standing"

        if kb.pressed(key.ESCAPE):
            arcade.close_window()

        if kb.pressed(key.F1):
            self.draw_collide = not self.draw_collide

        # if self.keyboard.down(key.UP) and self.player.jumping == False:
        #     moved = True
        #     self.player.jumping = True
        #     self.player.vel_y = -7

        # # if self.keyboard.down(K_DOWN):
        #     # moved = True

        # if self.keyboard.down(key.LEFT):
        #     moved = True
        #     self.move_left()
        # if self.keyboard.down(key.RIGHT):
        #     moved = True
        #     self.move_right()

        


        # # Handle joystick input
        # # if self.joystick is not None:
        # #     jx, jy = self.joystick.get_hat(0)
        # #     if jy > 0:
        # #         moved = True
        # #         self.move_up()
        # #     if jy < 0:
        # #         moved = True
        # #         self.move_down()
        # #     if jx < 0:
        # #         moved = True
        # #         self.move_left()
        # #     if jx > 0:
        # #         moved = True
        # #         self.move_right()

        # if moved:
        #     self.player.curr_state_key = "walking"
        # else:
        #     self.player.curr_state_key = "standing"
        super().update(delta_time*1000.0, context)

class PlayState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)

        self.running = True
        self.score = 0
        
        self.player = Player()
        self.camera = remgine.Camera(context)

        # self.GoombaWalk = remgine.Frames(SpriteSheet, [
        #     remgine.Frame(150, (510, 423, 32, 30)),
        #     remgine.Frame(150, (574, 359, 32, 30)),
        #     remgine.Frame(150, (544, 391, 32, 30))
        # ])
        
        # def on_goomba_killed(context, actor):
        #     print("Goomba killed!!")
        #     context.group.remove(actor)

        # self.GoombaDie = remgine.Frames(SpriteSheet, [
        #         remgine.Frame(150, (506, 354, 32, 30)),
        #         remgine.Frame(150, (540, 327, 32, 30)),
        #         remgine.Frame(150, (540, 359, 32, 30)),
        #         remgine.Frame(150, (574, 327, 32, 30)),
        #         remgine.Frame(150, (510, 391, 32, 30)),
        #         remgine.Frame(150, (318, 425, 32, 32))
        #     ], 
        #     next_state=None, 
        #     play_type=remgine.PlayType.Once,
        #     on_done=on_goomba_killed
        #   )

        # self.CoinFrames = remgine.Frames(SpriteSheet, [
        #     remgine.Frame(100, (0, 448, 16, 16)),
        #     remgine.Frame(100, (18, 448, 16, 16)),
        #     remgine.Frame(100, (36, 448, 16, 16)),
        #     remgine.Frame(100, (54, 448, 16, 16)),
        # ])

        self.map = remgine.tile_map.TileMap("../assets/level1.tmx", "main_layer")

        # level_script = self.tmxdata.properties["start_script"]
        # if level_script is not None:
        #     print("Got a level script from the level: " + level_script)
        #     level_module = importlib.import_module(level_script)
        #     level_module.start()
        # self.map_data = pyscroll.TiledMapData(self.tmxdata)
        # self.main_tiles = self.tmxdata.get_layer_by_name("main_layer")
        
        # self.map_layer = pyscroll.BufferedRenderer(self.map_data, (ScreenWidth, ScreenHeight), clamp_camera=False)
        # self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        # self.group.add(self.player)

        # Create an object grid and register our map objects into it.
        # self.collectible_obj_grid = self.create_obj_grid("collectible_objects")
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
            print("Inserting object {} at {}, {} with name {}, from {}".format(obj.name, obj.x, obj.y, obj.name, layer_name))
            if obj.name == "coin":
                obj.sprite = remgine.Actor({"normal": self.CoinFrames}, "normal", (obj.x, obj.y))
                obj.sprite.scale = 2
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

    def check_obj_collisions(self, objs):
        if len(objs) > 0:
            for o in objs:
                print("Hit object: " + o.name)
                if o.name == "coin" and o.sprite in self.group:
                    self.score += 100
                    self.group.remove(o.sprite)
                if o.name == "ghost" and o.sprite in self.group:
                    if o.sprite.curr_state_key != "killed":
                        o.sprite.curr_state_key = "killed"

    def update(self, delta_time):
        if self.context.keyboard.pressed(key.GRAVE):
            self.context.overlay_components["console"].toggle_active()

        kb = self.context.keyboard

        if kb.down(key.J):
            self.context.scroll_x -= 4
        if kb.down(key.L):
            self.context.scroll_x += 4
        if kb.down(key.I):
            self.context.scroll_y += 4
        if kb.down(key.K):
            self.context.scroll_y -= 4

        self.player.update(delta_time, self.context, self.map, self.camera)
        self.camera.update(delta_time)

        # if self.keyboard.pressed(key.SPACE):
        #     obj_list = self.interaction_obj_grid.get_from_points([
        #             self.player.rect.topleft,
        #             self.player.rect.topright,
        #             self.player.rect.bottomleft,
        #             self.player.rect.bottomright
        #         ])
            
        #     for o in obj_list:
        #         logging.info("Interacted with {}".format(o))
        #         if o.type == "hint":
        #             print("Hint: {}".format(o.properties["hint_text"]))


    def render(self):
        self.map.draw(0, 2)
        self.player.draw()
        self.map.draw(2, -1)
        
        # map_offset = (self.player.rect.x-ScreenWidth/2, self.player.rect.y-ScreenHeight/2)
        # for r in self.debug_rects:
        #     pygame.draw.rect(self.off_screen, (255,255,255), r.move((-map_offset[0], -map_offset[1])), width=1)

        # TODO: txt = self.font.render("Score: " + str(self.score), False, pygame.Color('white'))

def teleport(x, y, context):
    print(f"Moving player to tile {x}, {y}")
    play_state = context.curr_game_state
    player = play_state.player
    player.position = (x*32, y*32)

if __name__ == "__main__":
    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight),
            title="Tile scroller test"
        )
    
    context.game_states["play_state"] = PlayState(context)
    context.curr_game_state_key = "play_state"

    console = remgine.console.Console(context)
    context.overlay_components["console"] = console

    def console_callback(line, context):
        print(f"Got line: {line}")
        m = re.match("teleport (\d+),? (\d+)\s*", line)
        if m:
            print("Teleporting player!")
            teleport(int(m.group(1)), int(m.group(2)), context)

    console.callback = console_callback

    context.setup()
    arcade.run()
