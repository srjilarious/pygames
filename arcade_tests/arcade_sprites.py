import sys
sys.path.append("..")

import arcade
import arcade.key as key
import remgine

WindowWidth = 1280
WindowHeight = 720
ScreenWidth = 360
ScreenHeight = 180

class MainState(remgine.GameState):
    def __init__(self, context):
        super().__init__(context)
        self.rect = arcade.create_rectangle_filled(ScreenWidth/2, ScreenHeight/2, ScreenWidth, ScreenHeight, (100, 100, 220))
        self.sprite = arcade.Sprite(None, center_x=ScreenWidth/2, center_y = ScreenHeight/2)
        self.frames = arcade.load_textures("../actor_test/ramona_test.png", [
                (0, 182, 54, 67),
                (54, 182, 54, 67),
                (108, 182, 54, 67),
                (162, 182, 54, 67),
                (392, 0, 54, 67),
                (216, 182, 54, 67),
                (446, 0, 54, 67),
                (270, 182, 54, 67),
            ])

        self.sprite.texture = self.frames[0]
        self.frame_idx = 0
        self.frame_time = 0
    def update(self, delta_time):
        self.frame_time += delta_time
        if self.frame_time > 0.1:
            self.frame_idx = (self.frame_idx + 1) % 8
            self.frame_time = 0
            self.sprite.texture = self.frames[self.frame_idx]

    def render(self):
        self.rect.draw()
        self.sprite.draw()

class StateComponent(remgine.GameComponent):

    def update(self, delta_time):
        kb = self.context.keyboard
        if kb.pressed(key.F1):
            self.context.curr_game_state_key = "blue"
        elif kb.pressed(key.F2):
            self.context.curr_game_state_key = "red"
        elif kb.pressed(key.ESCAPE):
            arcade.close_window()

if __name__ == "__main__":

    context = remgine.GameContext(
            win_size=(WindowWidth, WindowHeight), 
            screen_size=(ScreenWidth, ScreenHeight),
            title="Game State Example"
        )
    
    context.game_states["main"] = MainState(context)
    context.curr_game_state_key = "main"
    context.components["global_keys"] = StateComponent(context)

    arcade.run()
