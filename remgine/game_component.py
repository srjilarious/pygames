class GameComponent:

    def __init__(self, context):
        self.context = context
        self._activated = False

    def update(self):
        pass

    def render(self):
        pass
    
    @property
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, value):
        self._activated = value