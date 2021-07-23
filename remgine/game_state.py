
class GameState:

    def __init__(self, context):
        self.context = context
        self.setup_done = False
        
    def on_pause_changed(self, new_paused_value):
        pass

    def setup(self):
        self.setup_done = True
        pass

    def update(self, delta_time):
        pass

    def render(self):
        pass
    