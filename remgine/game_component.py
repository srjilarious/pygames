class GameComponent:

    def __init__(self, context):
        self.context = context
        self._activated = False
        self.setup_done = False

    def setup(self):
        self.setup_done = True

    def update(self, delta_time):
        pass

    def render(self):
        pass
    
    @property
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, value):
        self._activated = value