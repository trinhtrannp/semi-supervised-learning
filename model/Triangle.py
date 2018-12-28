from plotly.utils import numpy

from model.Angle import Angle
from model.Line import Line
import math


class Triangle(object):

    def __init__(self, point1, point2, point3):
        self.A = point1
        self.B = point2
        self.C = point3

        self.__calculate_edges()
        self.__calculate_angles()
        self.__calculate_ratios()

    def is_real_triangle(self):
        has_0_angle = self.alpha.deg == 0 or self.beta.deg == 0 or self.gamma.deg == 0
        has_180_angle = self.alpha.deg == 180 or self.beta.deg == 180 or self.gamma.deg == 180
        return not has_0_angle and not has_180_angle

    def __calculate_edges(self):
        self.AB = Line(self.A, self.B)
        self.AC = Line(self.A, self.C)
        self.BC = Line(self.B, self.C)

        # a is length of the edge opposite to point A
        self.a = self.BC.length()

        # b is length of the edge opposite to point B
        self.b = self.AC.length()

        # c is length of the edge opposite to point C
        self.c = self.AB.length()

    def __calculate_angles(self):
        # print "alpha = ", math.acos(((self.b ** 2 + self.c ** 2) - self.a ** 2) / (2 * self.b * self.c))
        # print "beta = ", math.acos(((self.a ** 2 + self.c ** 2) - self.b ** 2) / (2 * self.a * self.c))
        # print "gamma = ", math.acos(((self.a ** 2 + self.b ** 2) - self.c ** 2) / (2 * self.a * self.b))
        # alpha is the angle at point A
        self.alpha = Angle(radian=math.acos(((self.b ** 2 + self.c ** 2) - self.a ** 2) / (2 * self.b * self.c)))

        # beta is the angle at to point B
        self.beta = Angle(radian=math.acos(((self.a ** 2 + self.c ** 2) - self.b ** 2) / (2 * self.a * self.c)))

        # gamma is the angle at to point C
        self.gamma = Angle(radian=math.acos(((self.a ** 2 + self.b ** 2) - self.c ** 2) / (2 * self.a * self.b)))

    def __calculate_ratios(self):
        """
        r1, r2, r3 are assure to always be greater than or equal 1
        """
        self.r1 = max(self.a, self.b) / min(self.a, self.b)
        self.r2 = max(self.a, self.c) / min(self.a, self.c)
        self.r3 = max(self.b, self.c) / min(self.b, self.c)

    def to_numpy_array(self):
        return numpy.array([self.A.to_xy_list(), self.B.to_xy_list(), self.C.to_xy_list()])
