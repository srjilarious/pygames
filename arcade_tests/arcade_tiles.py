"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import random

from pyglet.gl import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"
NumParticles = 10

class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)
        
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.wall_list = None
        self.dot_list = None
        
        
        

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """

        self.ball_list = arcade.SpriteList()
        # Name of map file to load
        map_name = "../remman/assets/level1.tmx"
        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'main_layer'
        # Name of the layer that has items for pick-up
        dots_layer_name = 'dots'

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=4,
                                                      use_spatial_hash=True)

        self.dot_list = arcade.tilemap.process_layer(my_map, dots_layer_name, 4)

        for i in range(NumParticles):
            ball = arcade.Sprite("../assets/blue_piece.png", 1)
            ball.center_x = random.randrange(SCREEN_WIDTH)
            ball.center_y = random.randrange(SCREEN_HEIGHT)
            ball.vel_x = random.randrange(-500, 500)
            ball.vel_y = random.randrange(-500, 500)
            self.ball_list.append(ball)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        # glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        self.wall_list.draw()
        self.dot_list.draw()
        self.ball_list.draw()
        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        for b in self.ball_list:
            b.center_x += b.vel_x*delta_time
            if b.center_x < 0 or b.center_x > SCREEN_WIDTH:
                b.vel_x = -b.vel_x

            b.center_y += b.vel_y*delta_time
            if b.center_y < 0 or b.center_y > SCREEN_HEIGHT:
                b.vel_y = -b.vel_y

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
