
class ObjectGrid:

    def __init__(self, cols, rows, tile_w, tile_h):
        # Create a 2d array of lists where we can store object references
        self._arr = [[[] for i in range(cols)] for j in range(rows)]
        self.tile_width = tile_w
        self.tile_height = tile_h

    def get(self, tile_col, tile_row):
        """Returns any objects registered at the tile col/row"""
        return self._arr[tile_row][tile_col]
    
    def set(self, tile_col, tile_row, l):
        """Sets the objects at the tile col/row to be the given list"""
        self._arr[tile_row][tile_col] = l

    def remove(self, obj, tile_col, tile_row):
        """Removes an object registered at the tile col/row"""
        l = self._arr[tile_row][tile_col]
        if obj in l:
            l.remove(obj)

    def insert_obj(self, rect, gid):
        """Takes a rectangle in world coordinates and inserts the object into the tile cells"""
        start_tx = int(rect[0] / self.tile_width)
        end_tx = int((rect[0] + rect[2]) / self.tile_width)
        start_ty = int(rect[1] / self.tile_height)
        end_ty = int((rect[1] + rect[3]) / self.tile_height)
        for y in range(start_ty, end_ty):
            for x in range(start_tx, end_tx):
                self._arr[y][x].append(gid)

    def tile_pos(self, point):
        """Converts a world coord point tuple into a tile coord point tuple"""
        return (int(point[0] / self.tile_width), int(point[1] / self.tile_height))

    def get_from_points(self, points):
        """Gets a list of objects, with dups removed, taking in world coordinates.
           points: A list of tuples in world coord space.
        """
        obj_list = list()
        for wc_p in points:
            tc_p = self.tile_pos(wc_p)
            obj_list = obj_list + self.get(tc_p[0], tc_p[1])

        if len(obj_list) > 0:
            # Remove dups
            obj_list = list(set(obj_list))

        return obj_list