import sys
sys.path.append("..")

import arcade
import arcade.key as key
import remgine

WindowWidth = 1920
WindowHeight = 1080
ScreenWidth = 192
ScreenHeight = 108

class BlueState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)
        self.rect = arcade.create_rectangle_filled(ScreenWidth/2, ScreenHeight/2, ScreenWidth, ScreenHeight, (0, 0, 255))
    def render(self):
        self.rect.draw()

class RedState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)
        self.rect = arcade.create_rectangle_filled(ScreenWidth/2, ScreenHeight/2, ScreenWidth, ScreenHeight, (255, 0, 0))

    def render(self):
        self.rect.draw()

class StateComponent(remgine.GameComponent):

    def update(self):
        if self.context.keyboard.pressed(key.F1):
            self.context.curr_game_state_key = "blue"
        elif self.context.keyboard.pressed(key.F2):
            self.context.curr_game_state_key = "red"

if __name__ == "__main__":

    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight),
            title="Game State Example"
        )
    
    context.game_states["blue"] = BlueState(context)
    context.game_states["red"] = RedState(context)
    context.curr_game_state_key = "blue"
    context.components["global_keys"] = StateComponent(context)

    arcade.run()
