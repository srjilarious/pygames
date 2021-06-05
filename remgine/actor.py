import pygame

class Frame:
    def __init__(self, time, rect):
        self.time = time
        self.rect = rect
        self.surface = None

class Frames:
    def __init__(self, sprite_sheet, frames):
        self.frames = frames
        self.sprite_sheet = sprite_sheet

        # Create subsurfaces referencing our main spritesheet surface
        for i, frame in enumerate(self.frames):
            frame.surface = self.sprite_sheet.subsurface(frame.rect)

class Actor(pygame.sprite.Sprite):
    def __init__(self, states={}, curr_state_key=None, position=(0,0)):
        pygame.sprite.Sprite.__init__(self)

        self.states = states
        self.curr_state_key = curr_state_key
        if self.curr_state_key is None or self.curr_state_key not in self.states:
            # Grab the first key from the states dictionary.
            self.curr_state_key = next(iter(self.states.keys()))

        self.curr_frame_idx = 0
        self.curr_frame_time = 0
        self.position = position
        self.layer = 0

    @property
    def curr_state(self):
        return self.states[self.curr_state_key]

    @property 
    def curr_frame(self):
        return self.curr_state.frames[self.curr_frame_idx]

    @property
    def image(self):
        return self.curr_frame.surface

    @property
    def rect(self):
        return pygame.Rect(self.position, (self.curr_frame.rect[2], self.curr_frame.rect[3]))

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)

    def update(self, time_elapsed_ms):
        self.curr_frame_time += time_elapsed_ms
        if self.curr_frame_time > self.curr_frame.time:
            self.curr_frame_time -= self.curr_frame.time
            self.curr_frame_idx += 1
            if self.curr_frame_idx >= len(self.curr_state.frames):
                self.curr_frame_idx = 0