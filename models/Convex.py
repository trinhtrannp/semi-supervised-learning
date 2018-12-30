from plotly.utils import numpy

from models.Angle import Angle
from models.Line import Line

from utils import geometry


class Convex(object):

    def __init__(self, point1, point2, point3, point4):
        self.__assign_points(point1, point2, point3, point4)

        self.__calculate_edges()
        self.__calculate_angles()
        self.__calculate_ratios()

    def __assign_points(self, point1, point2, point3, point4):
        point_list = [point1, point2, point3, point4]
        point_list.sort(key=lambda point: point.x, reverse=False)
        left_pair = point_list[:2]
        right_pair = point_list[2:]
        left_pair.sort(key=lambda point: point.y, reverse=True)
        right_pair.sort(key=lambda point: point.y, reverse=True)
        self.A = left_pair[0]
        self.B = right_pair[0]
        self.C = right_pair[1]
        self.D = left_pair[1]

    def is_real_convex(self):
        if self.alpha is not None and self.beta is not None and self.gamma is not None:
            has_0_angle = self.alpha.deg == 0 or self.beta.deg == 0 or self.gamma.deg == 0 or self.delta.deg == 0
            has_180_angle = self.alpha.deg == 180 or self.beta.deg == 180 or self.gamma.deg == 180 or self.delta.deg == 180
            return not has_0_angle and not has_180_angle
        else:
            raise Exception('there is no alpha, beta, gamma, delta')

    def __calculate_edges(self):
        self.AB = Line(self.A, self.B)
        self.BC = Line(self.B, self.C)
        self.CD = Line(self.C, self.D)
        self.DA = Line(self.D, self.A)

        self.ab = self.AB.length()
        self.bc = self.BC.length()
        self.cd = self.CD.length()
        self.da = self.DA.length()

    def __calculate_ratios(self):
        """
        r1, r2, r3 are assure to always be greater than or equal 1
        """
        self.r1 = max(self.ab, self.bc) / min(self.ab, self.bc)
        self.r2 = max(self.bc, self.cd) / min(self.bc, self.cd)
        self.r3 = max(self.cd, self.da) / min(self.cd, self.da)

    def __calculate_angles(self):
        #try:
            # alpha is the angle at point A
            self.alpha = Angle(radian=geometry.point_angle_rad(self.A, self.B, self.D))

            # beta is the angle at to point B
            self.beta = Angle(radian=geometry.point_angle_rad(self.B, self.A, self.C))

            # gamma is the angle at to point C
            self.gamma = Angle(radian=geometry.point_angle_rad(self.C, self.B, self.D))

            # delta is the angle at point D
            self.delta = Angle(radian=geometry.point_angle_rad(self.D, self.A, self.C))

        #except ValueError as e:
        #    print "A = ", self.A.x, ", ", self.A.y
        #    print "B = ", self.B.x, ", ", self.B.y
        #    print "C = ", self.C.x, ", ", self.C.y
        #    print "D = ", self.D.x, ", ", self.D.y
        #    print e
        #    raise ValueError("cannot compute alpha, beta, gamma, delta")

    def to_numpy_array(self):
        return numpy.array([self.A.to_xy_list(), self.B.to_xy_list(), self.C.to_xy_list(), self.D.to_xy_list()])
