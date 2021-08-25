# Simple pygame program
import arcade
import arcade.key as key

import sys
sys.path.append("..")
import remgine

WindowWidth = 1280
WindowHeight = 720
ScreenWidth = 360
ScreenHeight = 180
PlayerStartX = 25
PlayerStartY = 25
Speed = 1

RamonaSheet = "ramona_test.png"

class PlayState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)

        self.rect = arcade.create_rectangle_filled(ScreenWidth/2, ScreenHeight/2, ScreenWidth, ScreenHeight, (100, 100, 220))

        self.player = remgine.Actor({
            "standing": remgine.Frames(RamonaSheet, 
            [ 
                remgine.Frame(400, (468, 124, 44, 65)),
                remgine.Frame(400, (468, 190, 44, 65), (1, 0), (-1, 0)),
            ], allows_flip_horz=True),
            "walking": remgine.Frames(RamonaSheet, 
            [ 
                remgine.Frame(100, (0, 182, 54, 67)),
                remgine.Frame(100, (54, 182, 54, 67)),
                remgine.Frame(100, (108, 182, 54, 67)),
                remgine.Frame(100, (162, 182, 54, 67)),
                remgine.Frame(100, (392, 0, 54, 67)),
                remgine.Frame(100, (216, 182, 54, 67)),
                remgine.Frame(100, (446, 0, 54, 67)),
                remgine.Frame(100, (270, 182, 54, 67)),
            ], allows_flip_horz=True),
            "hit": remgine.Frames(RamonaSheet, 
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
        })

        self.player.center_x = 180
        self.player.center_y = 90

        # self.font = pygame.font.Font(None, 15)
        # self.running = True

        # if pygame.joystick.get_count() > 0:
        #     self.joystick = joystick = pygame.joystick.Joystick(0)
        #     self.joystick.init()
        # else:
        #     self.joystick = None


    def move_up(self):
        self.player.center_y += Speed

    def move_down(self):
        self.player.center_y -= Speed

    def move_left(self):
        self.player.flip_horz = True
        self.player.center_x -= Speed

    def move_right(self):
        self.player.flip_horz = False
        self.player.center_x += Speed

    def update(self, delta_time):
        kb = self.context.keyboard
        if kb.pressed(key.A):
            self.player.curr_state_key = "standing"
        if kb.pressed(key.S):
            self.player.curr_state_key = "walking"
        if kb.down(key.D):
            self.player.curr_state_key = "hit"
        # pressed_keys = pygame.key.get_pressed()

        if self.player.curr_state_key != "hit":
            moved = False
            if kb.down(key.UP):
                moved = True
                self.move_up()
            if kb.down(key.DOWN):
                moved = True
                self.move_down()
            if kb.down(key.LEFT):
                moved = True
                self.move_left()
            if kb.down(key.RIGHT):
                moved = True
                self.move_right()
            if moved:
                self.player.curr_state_key = "walking"
            else:
                self.player.curr_state_key = "standing"

        #     if self.joystick is not None:
        #         jx, jy = self.joystick.get_hat(0)
        #         if jy > 0:
        #             moved = True
        #             self.move_up()
        #         if jy < 0:
        #             moved = True
        #             self.move_down()
        #         if jx < 0:
        #             moved = True
        #             self.move_left()
        #         if jx > 0:
        #             moved = True
        #             self.move_right()



        if kb.down(key.F):
            self.player.curr_state_key = "hit";
        if kb.pressed(key.ENTER):
            self.center_x = PlayerStartX
            self.center_y = PlayerStartY
        if kb.pressed(key.ESCAPE):
            arcade.close_window()

        self.player.update(delta_time*1000.0, self.context)

    def render(self):
        # Draw sprite to off_screen buffer
        self.rect.draw()
        self.player.draw()



if __name__ == "__main__":
    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight),
            title="Actor Example"
        )
    
    context.game_states["play_state"] = PlayState(context)
    context.curr_game_state_key = "play_state"
    # context.components["global_keys"] = StateComponent(context)
    context.setup()
    arcade.run()