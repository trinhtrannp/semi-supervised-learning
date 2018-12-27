import math


class Angle(object):
    def __init__(self, radian):
        self.rad = radian
        self.deg = math.degrees(self.rad)

    def __init__(self, degree):
        self.deg = degree
        self.rad = math.radians(self.deg)
