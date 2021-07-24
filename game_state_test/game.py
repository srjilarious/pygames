import sys
sys.path.append("..")

import arcade
import arcade.key as key
import remgine
import remgine.console

WindowWidth = 1280
WindowHeight = 720
ScreenWidth = 320
ScreenHeight = 180

class BlueState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)
        self.rect = arcade.create_rectangle_filled(ScreenWidth/2, ScreenHeight/2, ScreenWidth, ScreenHeight, (0, 0, 180))
    def render(self):
        self.rect.draw()

class RedState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)
        self.rect = arcade.create_rectangle_filled(ScreenWidth/2, ScreenHeight/2, ScreenWidth, ScreenHeight, (180, 0, 0))

    def render(self):
        self.rect.draw()

class StateComponent(remgine.GameComponent):

    def update(self, delta_time):
        if self.context.keyboard.pressed(key.F1):
            self.context.curr_game_state_key = "blue"
        elif self.context.keyboard.pressed(key.F2):
            self.context.curr_game_state_key = "red"
        elif self.context.keyboard.pressed(key.GRAVE):
            self.context.overlay_components["console"].toggle_active()

if __name__ == "__main__":

    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight),
            title="Game State Example"
        )
    
    context.game_states["blue"] = BlueState(context)
    context.game_states["red"] = RedState(context)
    context.curr_game_state_key = "blue"

    console = remgine.console.Console(context)
    context.overlay_components["console"] = console
    context.components["global_keys"] = StateComponent(context)
    
    context.setup()
    
    arcade.run()
