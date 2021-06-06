
class ObjectGrid:

    def __init__(self, cols, rows, tile_w, tile_h):
        # Create a 2d array of lists where we can store object references
        self._arr = [[[] for i in range(cols)] for j in range(rows)]
        self.tile_width = tile_w
        self.tile_height = tile_h

    def get(self, col, row):
        return self._arr[row][col]
    
    def insert_obj(self, rect, gid):
        """akes a rectangle in world coordinates and inserts the gid into the tile cells"""
        start_tx = int(rect[0] / self.tile_width)
        end_tx = int((rect[0] + rect[2]) / self.tile_width)
        start_ty = int(rect[1] / self.tile_height)
        end_ty = int((rect[1] + rect[3]) / self.tile_height)
        for y in range(start_ty, end_ty):
            for x in range(start_tx, end_tx):
                self._arr[y][x].append(gid)