
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
        self.keys = { UP: False, DOWN: False, LEFT:False, RIGHT:False, H:False, C:False, ENTER:False}

    def create_dot(self):
        cx = random.randrange(SCREEN_WIDTH)
        cy = random.randrange(SCREEN_HEIGHT)
        dot = arcade.Sprite("../assets/power_dot.png", 1)
        dot.center_x = cx
        dot.center_y = cy
        self.dot_list.append(dot)

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
            self.dot_list.clear()
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
        self.player.center_y = min(self.player.center_y + SPEED,  SCREEN_HEIGHT - PLAYER_RADIUS)

    def move_down(self):
        self.player.center_y = max(PLAYER_RADIUS, self.player.center_y - SPEED)

    def move_left(self):
        self.player.center_x = max(PLAYER_RADIUS, self.player.center_x - SPEED)

    def move_right(self):
        self.player.center_x = min(self.player.center_x + SPEED, SCREEN_WIDTH - PLAYER_RADIUS)


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


####-------------------------------------
# import math
# import random

# from pygame.locals import *



# class GameContext:
#     def __init__(self):
#         # Set up the drawing window
#         self.screen = pygame.display.set_mode([WindowWidth, WindowHeight], flags=HWSURFACE|DOUBLEBUF)
#         self.off_screen = pygame.surface.Surface((ScreenWidth, ScreenHeight))

#         self.font = pygame.font.Font(None, 15)
#         self.running = True
#         self.player_x = PlayerStartX
#         self.player_y = PlayerStartY
#         self.player_radius = 8
#         self.player_radius_sq = self.player_radius**2
#         self.dot_radius = 4
#         self.dot_radius_sq = self.dot_radius**2
#         self.score = 1234
#         self.dots = []

#         if pygame.joystick.get_count() > 0:
#             self.joystick = joystick = pygame.joystick.Joystick(0)
#             self.joystick.init()
#         else:
#             self.joystick = None
#     def create_dot(self):
#         if len(self.dots) < 5000:
#             self.dots += [(random.randint(0, ScreenWidth), random.randint(0, ScreenHeight))]

#     def check_collide(self, dot):
#         dist_sq = (dot[0] - self.player_x)**2 + (dot[1] - self.player_y)**2
#         if dist_sq < (self.dot_radius_sq + self.player_radius_sq):
#             return True
#         return False


#     def move_up(self):
#         self.player_y = max(self.player_radius, self.player_y - Speed)

#     def move_down(self):
#         self.player_y = min(self.player_y + Speed,  ScreenHeight - self.player_radius)

#     def move_left(self):
#         self.player_x = max(self.player_radius, self.player_x - Speed)

#     def move_right(self):
#         self.player_x = min(self.player_x + Speed, ScreenWidth - self.player_radius)

#     def update_game(self):
#         pressed_keys = pygame.key.get_pressed()

#         if pressed_keys[K_UP]:
#             self.move_up()
#         if pressed_keys[K_DOWN]:
#             self.move_down()
#         if pressed_keys[K_LEFT]:
#             self.move_left()
#         if pressed_keys[K_RIGHT]:
#             self.move_right()
#         if pressed_keys[K_RETURN]:
#             self.player_x = PlayerStartX
#             self.player_y = PlayerStartY
#         if pressed_keys[K_h]:
#             self.create_dot()
#         if pressed_keys[K_c]:
#             self.dots.clear()
#         if pressed_keys[K_ESCAPE]:
#             self.running = False


#         if self.joystick is not None:
#             jx, jy = self.joystick.get_hat(0)
#             if jy > 0:
#                 self.move_up()
#             if jy < 0:
#                 self.move_down()
#             if jx < 0:
#                 self.move_left()
#             if jx > 0:
#                 self.move_right()

#         # Check collisions with dots
#         for i, dot in enumerate(self.dots):
#             if self.check_collide(dot):
#                 self.score += 50
#                 del self.dots[i]

#     def render(self):
#         # Fill the background with white
#         self.off_screen.fill((0,0,0))

#         # Draw a solid blue circle in the center
#         pygame.draw.circle(self.off_screen, (0, 0, 255), (self.player_x, self.player_y), self.player_radius)

#         # Draw the dots
#         for i, dot in enumerate(self.dots):
#             pygame.draw.circle(self.off_screen, (255, 255, 0), (dot[0], dot[1]), self.dot_radius)

#         txt = self.font.render("Score: " + str(self.score), False, pygame.Color('white'))
#         self.off_screen.blit(txt, (5, 5))

#         self.screen.blit(pygame.transform.scale(self.off_screen, self.screen.get_rect().size), (0, 0))
#         # Flip the display
#         pygame.display.flip()


# if __name__ == "__main__":
#     pygame.init()
#     pygame.joystick.init()

#     context = GameContext()
    
#     for i in range(100):
#         context.create_dot()

#     while context.running:
#         # Did the user click the window close button?
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 context.running = False
#             elif event.type == VIDEORESIZE:
#                 context.screen = pygame.display.set_mode(event.size, flags=HWSURFACE|DOUBLEBUF)

#         context.update_game()
#         context.render()

#     # Done! Time to quit.
#     pygame.quit()