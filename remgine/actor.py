import pygame
from enum import Enum

class Frame:
    def __init__(self, time, rect):
        self.time = time
        self.rect = rect
        self.surface = None

class PlayType(Enum):
    Loop = 0
    Once = 1


class Frames:
    def __init__(self, sprite_sheet, frames, next_state=None, play_type=PlayType.Once):
        self.frames = frames
        self.sprite_sheet = sprite_sheet
        self.next_state_key = next_state
        self.play_type = play_type

        # Create subsurfaces referencing our main spritesheet surface
        for i, frame in enumerate(self.frames):
            frame.surface = self.sprite_sheet.subsurface(frame.rect)

class Actor(pygame.sprite.Sprite):
    def __init__(self, states={}, curr_state_key=None, position=(0,0)):
        pygame.sprite.Sprite.__init__(self)

        self.states = states
        self._curr_state_key = curr_state_key
        if self._curr_state_key is None or self._curr_state_key not in self.states:
            # Grab the first key from the states dictionary.
            self._curr_state_key = next(iter(self.states.keys()))

        self.curr_frame_idx = 0
        self.curr_frame_time = 0
        self.position = position
        self.flip_horz = False
        self.flip_vert = False
        self.layer = 0

    @property
    def curr_state(self):
        return self.states[self._curr_state_key]

    @property 
    def curr_frame(self):
        return self.curr_state.frames[self.curr_frame_idx]

    @property
    def image(self):
        return self.curr_frame.surface

    @property
    def rect(self):
        return pygame.Rect(self.position, (self.curr_frame.rect[2], self.curr_frame.rect[3]))

    @property
    def curr_state_key(self):
        return self._curr_state_key
    
    @curr_state_key.setter
    def curr_state_key(self, value):
        self._curr_state_key = value
        self.curr_frame_time = 0
        self.curr_frame_idx = 0

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)

    def draw(self, screen):
        if self.flip_horz or self.flip_vert:
            screen.blit(pygame.transform.flip(self.image, self.flip_horz, self.flip_vert), self.rect)
        else:
            screen.blit(self.image, self.rect)

    def update(self, time_elapsed_ms):
        self.curr_frame_time += time_elapsed_ms

        # Check if we should advance frames.
        if self.curr_frame_time > self.curr_frame.time:
            self.curr_frame_time -= self.curr_frame.time
            self.curr_frame_idx += 1

            # See if we reached the end of the state's frame list.
            if self.curr_frame_idx >= len(self.curr_state.frames):
                self.curr_frame_idx = 0

                # Check if this state transitions to another automatically.
                if (self.curr_state.play_type == PlayType.Once and
                    self.curr_state.next_state_key is not None):
                    self.curr_state_key = self.curr_state.next_state_key