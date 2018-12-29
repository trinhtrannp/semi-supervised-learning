import math


class Angle(object):

    rad = 0
    deg = 0

    def __init__(self, radian=None, degree=None):
        if radian is None and degree is None:
            raise Exception('input params cannot be all None')

        if radian is not None and degree is not None and not radian == math.radians(degree):
            raise Exception('input params should match each other')

        if radian:
            self.rad = radian
            self.deg = math.degrees(self.rad)

        if degree:
            self.deg = degree
            self.rad = math.radians(self.deg)
