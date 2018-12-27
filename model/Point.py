import math


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, pointB):
        dis = math.sqrt(math.pow(self.x - pointB.x, 2) - math.pow(self.y - pointB.y, 2))
        return dis
