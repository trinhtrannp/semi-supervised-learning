import math


class Angle(object):
    def __init__(self, radian=None, degree=None):
        if not radian and not degree:
            raise Exception('input params cannot be all None')

        if radian and degree and not radian == math.radians(degree):
            raise Exception('input params should match each other')

        if radian:
            self.rad = radian
            self.deg = math.degrees(self.rad)

        if degree:
            self.deg = degree
            self.rad = math.radians(self.deg)
