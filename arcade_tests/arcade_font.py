import sys
sys.path.append("..")

import arcade
import arcade.key as key

import pyglet.font

import remgine

WindowWidth = 1280
WindowHeight = 720
ScreenWidth = 360
ScreenHeight = 180

class MainState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)
        self.rect = arcade.create_rectangle_filled(ScreenWidth/2, ScreenHeight/2, ScreenWidth, ScreenHeight, (100, 200, 220))
        

    def update(self, delta_time):
        pass

    def render(self):
        self.rect.draw()
        # arcade.draw_text("Testing Testing!", 10, 10, (255, 255, 255), font_size=10, font_name="Monospace")

class FontOverlayComponent(remgine.GameComponent):

    def render(self):
        arcade.draw_text("Testing Testing!", 10, 10, (255, 255, 255), font_size=20, font_name="Monospace")


class StateComponent(remgine.GameComponent):

    def update(self, delta_time):
        kb = self.context.keyboard
        if kb.pressed(key.ESCAPE):
            arcade.close_window()

if __name__ == "__main__":

    # pyglet.font.add_file("AmigaTopaz1.ttf")
    # pyglet.font.add_directory(".")

    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight),
            title="Font Loading Example"
        )
    
    context.game_states["main"] = MainState(context)
    context.curr_game_state_key = "main"
    context.components["global_keys"] = StateComponent(context)
    context.overlay_components["text_overlay"] = FontOverlayComponent(context)

    arcade.run()
