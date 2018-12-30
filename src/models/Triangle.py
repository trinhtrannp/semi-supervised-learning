import numpy

from src.models.Angle import Angle
from src.models.Line import Line
import math

from src.utils import geometry


class Triangle(object):

    def __init__(self, point1, point2, point3):
        self.A = point1
        self.B = point2
        self.C = point3

        self.__calculate_edges()
        self.__calculate_angles()
        self.__calculate_ratios()

    def is_real_triangle(self):
        if self.alpha is not None and self.beta is not None and self.gamma is not None:
            has_0_angle = self.alpha.deg == 0 or self.beta.deg == 0 or self.gamma.deg == 0
            has_180_angle = self.alpha.deg == 180 or self.beta.deg == 180 or self.gamma.deg == 180
            return not has_0_angle and not has_180_angle
        else:
            raise Exception('there is not alpha, beta, gamma')

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
        try:
            # alpha is the angle at point A
            alpha_cos = geometry.clean_cos(((self.b ** 2 + self.c ** 2) - self.a ** 2) / (2 * self.b * self.c))
            self.alpha = Angle(radian=math.acos(alpha_cos))

            # beta is the angle at to point B
            beta_cos = geometry.clean_cos(((self.a ** 2 + self.c ** 2) - self.b ** 2) / (2 * self.a * self.c))
            self.beta = Angle(radian=math.acos(beta_cos))

            # gamma is the angle at to point C
            gamma_cos = geometry.clean_cos(((self.a ** 2 + self.b ** 2) - self.c ** 2) / (2 * self.a * self.b))
            self.gamma = Angle(radian=math.acos(gamma_cos))
        except ValueError:
            print "alpha = ", ((self.b ** 2 + self.c ** 2) - self.a ** 2) / (2 * self.b * self.c)
            print "beta  = ", ((self.a ** 2 + self.c ** 2) - self.b ** 2) / (2 * self.a * self.c)
            print "gamma = ", ((self.a ** 2 + self.b ** 2) - self.c ** 2) / (2 * self.a * self.b)
            print "A = ", self.A.x, ", ", self.A.y
            print "B = ", self.B.x, ", ", self.B.y
            print "C = ", self.C.x, ", ", self.C.y
            raise ValueError("cannot compute alpha, beta, gamma")

    def __calculate_ratios(self):
        """
        r1, r2, r3 are assure to always be greater than or equal 1
        """
        self.r1 = max(self.a, self.b) / min(self.a, self.b)
        self.r2 = max(self.a, self.c) / min(self.a, self.c)
        self.r3 = max(self.b, self.c) / min(self.b, self.c)

    def to_numpy_array(self):
        return numpy.array([self.A.to_xy_list(), self.B.to_xy_list(), self.C.to_xy_list()])
