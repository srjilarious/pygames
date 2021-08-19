
class Camera:
    def __init__(self, context):
        self.context = context

        self._max_vel_x = 8
        self._max_vel_y = 8

        self.small_dist = 150

        self.goal_x = 0
        self.goal_y = 0

    def update(self, delta_time_sec):
        curr_x = self.context.scroll_x
        curr_y = self.context.scroll_y

        dist_x = self.goal_x - curr_x
        dist_y = self.goal_y - curr_y
        adx = abs(dist_x)
        ady = abs(dist_y)

        if adx < self.small_dist:
            mx = (adx * self._max_vel_x // self.small_dist)
        else:
            mx = self._max_vel_x
        
        if ady < self.small_dist:
            my = (ady * self._max_vel_y // self.small_dist)
        else:
            my = self._max_vel_y
        

        amt_x = min(mx, adx)
        amt_y = min(my, ady)
        if dist_x < 0:
            amt_x = -amt_x
        
        if dist_y < 0:
            amt_y = -amt_y

        self.context.scroll_x = self.context.scroll_x + amt_x
        self.context.scroll_y = self.context.scroll_y + amt_y
    
