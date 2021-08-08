# Tile engine pygame test
import math
import random
import importlib
import logging
import sys

import arcade
import arcade.key as key

sys.path.append("..")
import remgine

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

class PlayState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)

        self.running = True
        self.score = 0
        
        self.player = remgine.Actor({
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

        self.player.position = (280,150)

        # self.player = remgine.Actor({
        #     "standing": remgine.Frames(SpriteSheet, 
        #     [ 
        #         remgine.Frame(400, (557, 0, 42, 65)),
        #         remgine.Frame(400, (557, 68, 42, 65), (1, 0), (-1, 0)),
        #     ]),
        #     "walking": remgine.Frames(SpriteSheet, 
        #     [ 
        #         remgine.Frame(100, (368, 296, 50, 65)),
        #         remgine.Frame(100, (302, 358, 50, 65)),
        #         remgine.Frame(100, (420, 256, 50, 65)),
        #         remgine.Frame(100, (354, 363, 50, 65)),
        #         remgine.Frame(100, (420, 323, 50, 65)),
        #         remgine.Frame(100, (406, 390, 50, 65)),
        #         remgine.Frame(100, (458, 390, 50, 65)),
        #         remgine.Frame(100, (505, 0, 50, 65)),
        #     ])
        # }, "standing", (100, 100))
        
        self.player.collide_adjust = (0, 0, 50, 60)
        # self.player.jumping = False
        # self.player.vel_y = 0

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

        # self.tmxdata = load_pygame("level1.tmx")

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

    # def tile_pos(self, point):
    #     return (int(point[0] / self.tmxdata.tilewidth), int(point[1] / self.tmxdata.tileheight))

    def move_up(self, amount = -Speed):
        pass
        # self.player_y = max(self.player_radius, self.player_y - Speed)
        # new_rect = self.player.collide_rect.move(0, amount)
        # ty = int(new_rect.top / self.tmxdata.tileheight)
        # tx_l = int(new_rect.left / self.tmxdata.tilewidth)
        # tx_r = int(new_rect.right / self.tmxdata.tilewidth)
        # if not self.check_collide_tile(new_rect, tx_l, ty) and not self.check_collide_tile(new_rect, tx_r, ty):
        #     # self.player.position = (new_rect.x, new_rect.y)
        #     self.player.position = (self.player.position[0], self.player.position[1] +amount)
        # else:
        #     self.player.position = (self.player.position[0], (ty+1)*self.tmxdata.tileheight)
        #     self.player.vel_y = 0

        # # Check object collisions
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx_l, ty))
        # self.check_obj_collisions(self.collectible_obj_grid.get(midpoint(tx_l, tx_r), ty))
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx_r, ty))
        
        
    def move_down(self, amount = Speed):
        pass
        # new_rect = self.player.collide_rect.move(0, amount)
        # ty = int(new_rect.bottom / self.tmxdata.tileheight)
        # tx_l = int(new_rect.left / self.tmxdata.tilewidth)
        # tx_r = int(new_rect.right / self.tmxdata.tilewidth)
        # if not self.check_collide_tile(new_rect, tx_l, ty) and not self.check_collide_tile(new_rect, tx_r, ty):
        #     # self.player.position = (new_rect.x, new_rect.y)
        #     self.player.position = (self.player.position[0], self.player.position[1] +amount)
        # else:
        #     self.player.position = (self.player.position[0], (ty)*self.tmxdata.tileheight -self.player.collide_rect[3])
        #     self.player.jumping = False
        #     self.player.vel_y = 0
        
        # # Check object collisions
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx_l, ty))
        # self.check_obj_collisions(self.collectible_obj_grid.get(midpoint(tx_l, tx_r), ty))
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx_r, ty))

    def move_left(self):
        pass
        # self.player.flip_horz = True
        # new_rect = self.player.collide_rect.move(-Speed, 0)
        # tx = int(new_rect.left / self.tmxdata.tilewidth)
        # ty_t = int(new_rect.top / self.tmxdata.tileheight)
        # ty_b = int(new_rect.bottom / self.tmxdata.tileheight)
        # if not self.check_collide_tile(new_rect, tx, ty_t) and not self.check_collide_tile(new_rect, tx, ty_b):
        #     # self.player.position = (new_rect.x, new_rect.y)
        #     self.player.position = (self.player.position[0]-Speed, self.player.position[1])
        # else:
        #     self.player.position = ((tx+1)*self.tmxdata.tileheight, self.player.position[1])

        # # Check object collisions
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx, ty_t))
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx, midpoint(ty_t, ty_b)))
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx, ty_b))

    def move_right(self):
        pass
        # self.player.flip_horz = False
        # new_rect = self.player.collide_rect.move(Speed, 0)
        # tx = int(new_rect.right / self.tmxdata.tilewidth)
        # ty_t = int(new_rect.top / self.tmxdata.tileheight)
        # ty_b = int(new_rect.bottom / self.tmxdata.tileheight)
        # if not self.check_collide_tile(new_rect, tx, ty_t) and not self.check_collide_tile(new_rect, tx, ty_b):
        #     # self.player.position = (new_rect.x, new_rect.y)
        #     self.player.position = (self.player.position[0]+Speed, self.player.position[1])
        # else:
        #     self.player.position = ((tx)*self.tmxdata.tileheight - 1 - self.player.collide_rect[2], self.player.position[1])

        # # Check object collisions
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx, ty_t))
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx, midpoint(ty_t, ty_b)))
        # self.check_obj_collisions(self.collectible_obj_grid.get(tx, ty_b))

    def update(self, delta_time):
        kb = self.context.keyboard

        if kb.down(key.J):
            self.context.scroll_x -= 4
        if kb.down(key.L):
            self.context.scroll_x += 4
        if kb.down(key.I):
            self.context.scroll_y += 4
        if kb.down(key.K):
            self.context.scroll_y -= 4

        if kb.down(key.UP):
            (_moved, self.player.position) = self.map.check_move_up(self.player, 4)
        if kb.down(key.DOWN):
            (_moved, self.player.position) = self.map.check_move_down(self.player, 4)
        if kb.down(key.LEFT):
            (_moved, self.player.position) = self.map.check_move_left(self.player, 4)
        if kb.down(key.RIGHT):
            (_moved, self.player.position) = self.map.check_move_right(self.player, 4)

        # moved = False
        # if kb.any_down([key.UP, key.DOWN, key.LEFT, key.RIGHT]):
        #     self.debug_rects.clear()

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

        # if self.player.vel_y < 5:
        #     self.player.vel_y += 0.1

        # if self.player.vel_y < 0:
        #     self.move_up(int(self.player.vel_y))
        # else:
        #     self.move_down(int(self.player.vel_y))


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

        # if self.keyboard.down(key.RETURN):
        #     self.player_x = PlayerStartX
        #     self.player_y = PlayerStartY
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

        # if self.keyboard.down(key.ESCAPE):
        #     self.running = False

        # for sp in self.group:
        #     sp.update(10, self)
        self.player.update(delta_time*1000.0, self.context)
        
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
            collide_rect = pygame.Rect(int(x*tw), int(y*th), tw, th)
            # Debug, draw collide rect.
            self.debug_rects.append(collide_rect)

            return player_rect.colliderect(collide_rect)
        else:
            return False

    def get_main_tile(self, x, y):
        return self.main_tiles.data[int(y)][int(x)]

    def render(self):
        self.map.draw()
        self.player.draw()
        # Fill the background with white
        # self.off_screen.fill((0,0,0))


        # self.group.center((self.player.rect.x, self.player.rect.y))
        #self.group.center((ScreenWidth/2, ScreenHeight/2))
        
        # self.group.draw(self.off_screen)
        
        # Draw a solid blue circle in the center
        # pygame.draw.circle(self.off_screen, (0, 0, 255), (self.player_x, self.player_y), self.player_radius)
        # p_screen_pos = pygame.Rect(ScreenWidth/2, ScreenHeight/2, PlayerWidth, PlayerHeight)
        # pygame.draw.rect(self.off_screen, (0,0,255), p_screen_pos)

        #pygame.draw.rect(self.off_screen, (0,0,255), self.player.rect)

        # map_offset = (self.player.rect.x-ScreenWidth/2, self.player.rect.y-ScreenHeight/2)
        # for r in self.debug_rects:
        #     pygame.draw.rect(self.off_screen, (255,255,255), r.move((-map_offset[0], -map_offset[1])), width=1)

        # TODO: txt = self.font.render("Score: " + str(self.score), False, pygame.Color('white'))
        pass



if __name__ == "__main__":
    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight),
            title="Tile scroller test"
        )
    
    context.game_states["play_state"] = PlayState(context)
    context.curr_game_state_key = "play_state"
    context.setup()
    arcade.run()
