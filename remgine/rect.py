from dataclasses import dataclass

@dataclass
class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    @property
    def left(self):
        return self.x
    
    @property
    def right(self):
        return self.x + self.w
    
    @property
    def top(self):
        return self.y
    
    @property
    def bottom(self):
        return self.y + self.h

    def move(self, x, y):
        return Rect(self.x+x, self.y+y, self.w, self.h)
    
    def colliderect(self, rect):
        if ((self.left < rect.right) and
           (self.right > rect.left) and
           (self.top < rect.bottom) and
           (self.bottom > rect.top)):
            return True
        return False