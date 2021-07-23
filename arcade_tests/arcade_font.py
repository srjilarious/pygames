import sys
sys.path.append("..")

import arcade
import arcade.key as key

import pyglet.font
import pyglet.text

import remgine

WindowWidth = 1280
WindowHeight = 720
ScreenWidth = 360
ScreenHeight = 180

class MainState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)
        self.rect = arcade.create_rectangle_filled(ScreenWidth/2, ScreenHeight/2, ScreenWidth, ScreenHeight, (100, 200, 220))
        self.ball = arcade.Sprite("../assets/blue_piece.png", 1)

    def update(self, delta_time):
        pass

    def render(self):
        self.rect.draw()
        # arcade.draw_text("Testing Testing!", 10, 10, (255, 255, 255), font_size=10, font_name="Monospace")

class FontOverlayComponent(remgine.GameComponent):

    def __init__(self, context):
        super().__init__(context)
        self.text = None


    def setup(self):
        from ctypes import c_int
        from pyglet.gl import glGetIntegerv, GL_MAX_TEXTURE_SIZE

        i = c_int()
        glGetIntegerv(GL_MAX_TEXTURE_SIZE, i)
        print(i)

        self.font = pyglet.font.load('DejaVu Sans Mono', 14, bold=True, italic=False)
        print(pyglet.font.have_font("DejaVu Sans Mono"))
        print(pyglet.font.have_font("Inconsolata"))
        print(pyglet.font.have_font("Amiga Topaz Unicode Rus2"))
        print(pyglet.font.have_font("Amiga Topaz Unicode Rus"))
        
        # self.text = pyglet.text.Label("My text label!")
        # self.text = pyglet.text.Label('Hello, world', font_name="Amiga Topaz Unicode Rus", font_size=20)
        # self.label = pyglet.text.Label('Hello, world',
        #                 # font_name='DejaVu Sans Mono',
        #                 font_size=36,
        #                 x=100, y=100)
        
    def render(self):
        # arcade.draw_text("Testing Testing!", 10, 10, (255, 255, 255), font_size=12, font_name="AmigaTopaz.ttf")
        arcade.draw_text("Testing Testing!", 10, 10, (255, 255, 255), font_size=30, font_name="../assets/Inconsolata-Regular.ttf")
        # arcade.draw_text("Testing Testing!", 10, 10, (255, 255, 255), font_size=20, font_name="DejaVu Sans Mono")
        # arcade.draw_text("Testing Testing!", 10, 50, (255, 255, 255), font_size=30)
        # self.text.draw()
        # self.label.draw()
        # arcade.draw_text("Testing 2!", 10, 10, (255, 255, 255), font_size=20, font_name="Inconsolata")


class StateComponent(remgine.GameComponent):

    def update(self, delta_time):
        kb = self.context.keyboard
        if kb.pressed(key.ESCAPE):
            arcade.close_window()

if __name__ == "__main__":

    # pyglet.font.add_directory(".")

    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight),
            title="Font Loading Example"
        )
    
    # pyglet.font.add_file("../assets/Inconsolata-Regular.ttf")
    # pyglet.font.add_file("./AmigaTopaz.ttf")

    context.game_states["main"] = MainState(context)
    context.curr_game_state_key = "main"
    context.components["global_keys"] = StateComponent(context)
    context.overlay_components["text_overlay"] = FontOverlayComponent(context)
    
    context.setup()

    arcade.run()
