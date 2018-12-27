class Line(object):

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def length(self):
        return self.point1.distance_to(pointB=self.point2)
