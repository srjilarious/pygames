
# Blue circle eats yellow circles
"""
Arcade program to use an offscreen buffer for pixely scaling.
"""
import random

import arcade
from arcade.gl import geometry
from arcade.key import *
from pyglet.gl import *

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
SCREEN_WIDTH = 192
SCREEN_HEIGHT = 108
SCREEN_TITLE = "Blue dot must FEED!"
NUM_PARTICLES = 100

PLAYER_START_X = 25
PLAYER_START_Y = 25

PLAYER_RADIUS = 8
DOT_RADIUS = 4
RADIUS_CHECK = (PLAYER_RADIUS**2 + DOT_RADIUS**2)

SPEED = 0.5


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.dot_list = None
        self.player = None
        self.score = 0
        self.keys = { UP: False, DOWN: False, LEFT:False, RIGHT:False, H:False, C:False, F:False, ENTER:False, ESCAPE:False}

    def create_dot(self, cx=None, cy=None):

        if cx is None:
            cx = random.randrange(SCREEN_WIDTH)
        if cy is None:
            cy = random.randrange(SCREEN_HEIGHT)

        dot = arcade.Sprite("../assets/power_dot.png", 1)
        dot.center_x = cx
        dot.center_y = cy
        self.dot_list.append(dot)
        return dot

    def setup(self):
        self.dot_list = arcade.SpriteList()

        for i in range(NUM_PARTICLES):
            self.create_dot()

        self.player = arcade.Sprite("../assets/blue_ghost.png", 1)
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y
        
    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        arcade.set_viewport(0,
                            SCREEN_WIDTH,
                            0,
                            SCREEN_HEIGHT
                            )

        self.dot_list.draw(filter=GL_NEAREST)

        self.player.draw()

    def on_update(self, delta_time):
        if self.keys[UP]:
            self.move_up()
        if self.keys[DOWN]:
            self.move_down()
        if self.keys[LEFT]:
            self.move_left()
        if self.keys[RIGHT]:
            self.move_right()
        if self.keys[ENTER]:
            self.player.center_x = PLAYER_START_X
            self.player.center_y = PLAYER_START_Y
        if self.keys[H]:
            self.create_dot()
        if self.keys[C]:
            for d in self.dot_list:
                d.kill()
        if self.keys[F]:
            for y in range(0, SCREEN_HEIGHT, DOT_RADIUS):
                for x in range(0, SCREEN_WIDTH, DOT_RADIUS):
                    self.create_dot(x, y)
        if self.keys[ESCAPE]:
            arcade.close_window()
            
        # if pressed_keys[K_ESCAPE]:
        #     self.running = False
    
        # Check collisions with dots
        for i, dot in enumerate(self.dot_list):
            if self.check_collide(dot):
                self.score += 50
                dot.kill()

    def check_collide(self, dot):
        dist_sq = (dot.center_x - self.player.center_x)**2 + (dot.center_y - self.player.center_y)**2
        if dist_sq < RADIUS_CHECK:
            return True
        return False


    def move_up(self):
        self.player.center_y = min(self.player.center_y + SPEED,  SCREEN_HEIGHT + PLAYER_RADIUS)

    def move_down(self):
        self.player.center_y = max(-PLAYER_RADIUS, self.player.center_y - SPEED)

    def move_left(self):
        self.player.center_x = max(-PLAYER_RADIUS, self.player.center_x - SPEED)

    def move_right(self):
        self.player.center_x = min(self.player.center_x + SPEED, SCREEN_WIDTH + PLAYER_RADIUS)


    def on_key_press(self, key, key_modifiers):
        if key in self.keys:
            self.keys[key] = True

    def on_key_release(self, key, key_modifiers):
        if key in self.keys:
            self.keys[key] = False



def main():
    """ Main method """
    game = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
