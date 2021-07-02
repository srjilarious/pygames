import pygame
from enum import Enum

class Frame:
    def __init__(self, time, rect, gravity=(0,0), left_gravity=(0,0)):
        self.time = time
        self.rect = rect
        self.gravity = gravity
        # Hack, should center drawing
        self.left_gravity = left_gravity
        self.surface = None

class PlayType(Enum):
    Loop = 0
    Once = 1


class Frames:
    def __init__(self, sprite_sheet, frames, next_state=None, play_type=PlayType.Loop, on_done=None):
        self.frames = frames
        self.sprite_sheet = sprite_sheet
        self.next_state_key = next_state
        self.play_type = play_type
        self.on_done = on_done

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
        self.collide_scale = None
        self.render_scale = None
        self.layer = 0
        self.collide_adjust = (0, 0, 0, 0)
    @property
    def curr_state(self):
        return self.states[self._curr_state_key]

    @property 
    def curr_frame(self):
        return self.curr_state.frames[self.curr_frame_idx]

    @property
    def image(self):
        surf = self.curr_frame.surface

        if self.render_scale is not None:
            surf = pygame.transform.scale(surf, ((int(self.curr_frame.rect[2]*self.render_scale), int(self.curr_frame.rect[3]*self.render_scale))))

        if self.flip_horz or self.flip_vert:
            surf = pygame.transform.flip(surf, self.flip_horz, self.flip_vert)
        
        return surf

    @property
    def collide_rect(self):
        r = pygame.Rect(self.position[0]+self.collide_adjust[0], 
                        self.position[1]+self.collide_adjust[1], 
                        self.collide_adjust[2], 
                        self.collide_adjust[3])
        if self.collide_scale is not None:
            r = pygame.Rect(r.topleft, (int(r.width*self.collide_scale), int(r.height*self.collide_scale)))
        return r

    @property
    def rect(self):
        if self.render_scale is not None:
            return pygame.Rect(self.draw_position, (int(self.curr_frame.rect[2]*self.render_scale), int(self.curr_frame.rect[3]*self.render_scale)))
        else:
            return pygame.Rect(self.draw_position, (self.curr_frame.rect[2], self.curr_frame.rect[3]))

    @property
    def draw_position(self):
        if(self.flip_horz):
            return (self.position[0] - self.curr_frame.left_gravity[0], self.position[1] - self.curr_frame.left_gravity[1])
        else:
            return (self.position[0] - self.curr_frame.gravity[0], self.position[1] - self.curr_frame.gravity[1])

    @property
    def curr_state_key(self):
        return self._curr_state_key
    
    @curr_state_key.setter
    def curr_state_key(self, value):
        if self._curr_state_key != value:
            self._curr_state_key = value
            self.reset_state()

    def reset_state(self):
        self.curr_frame_time = 0
        self.curr_frame_idx = 0

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)

    def draw(self, screen):
        screen.blit(self.image, self.draw_position)

    def update(self, time_elapsed_ms, context):
        self.curr_frame_time += time_elapsed_ms

        # Check if we should advance frames.
        if self.curr_frame_time > self.curr_frame.time:
            self.curr_frame_time -= self.curr_frame.time
            self.curr_frame_idx += 1

            # See if we reached the end of the state's frame list.
            if self.curr_frame_idx >= len(self.curr_state.frames):
                self.curr_frame_idx = 0

                # Check if this state transitions to another automatically.
                if self.curr_state.play_type == PlayType.Once:

                    # Check for a state finished task
                    if self.curr_state.on_done is not None:
                        self.curr_state.on_done(context, self)

                    if self.curr_state.next_state_key is not None:
                        self.curr_state_key = self.curr_state.next_state_key