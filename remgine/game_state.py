
class GameState:

    def __init__(self, context):
        self.context = context

    def on_pause_changed(self, new_paused_value):
        pass

    def update(self, delta_time):
        pass

    def render(self):
        pass
    