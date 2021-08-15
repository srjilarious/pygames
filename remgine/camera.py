
class Camera:
    def __init__(self, context):
        self.context = context
        self._max_vel_x = 3
        self._max_vel_y = 3

        self.goal_x = 0
        self.goal_y = 0

    def update(self, delta_time_sec):
        curr_x = self.context.scroll_x
        curr_y = self.context.scroll_y

        dist_x = self.goal_x - curr_x
        dist_y = self.goal_y - curr_y

        amt_x = min(self._max_vel_x, abs(dist_x))
        amt_y = min(self._max_vel_y, abs(dist_y))
        if dist_x < 0:
            amt_x = -amt_x
        
        if dist_y < 0:
            amt_y = -amt_y

        self.context.scroll_x = self.context.scroll_x + amt_x
        self.context.scroll_y = self.context.scroll_y + amt_y
    
