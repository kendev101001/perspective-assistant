
class FocalPoint():
    def __init__(self, focal_point_index):
        self.focal_point_index = focal_point_index
        self.position_x, self.position_y = 0, 0

    def setPosition(self, position_x, position_y):
        self.position_x, self.position_y = position_x, position_y