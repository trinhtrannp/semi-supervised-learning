import itertools
import random

from src.models.Point import Point
from src.models import Triangle


class TriangleGenerator(object):

    def __init__(self, X_lowerbound, X_uperbound, Y_lowerbound, Y_uperbound, X_resolution, Y_resolution):
        self.X_lowerbound = X_lowerbound
        self.X_uperbound = X_uperbound
        self.Y_lowerbound = Y_lowerbound
        self.Y_uperbound = Y_uperbound
        self.X_resolution = X_resolution
        self.Y_resolution = Y_resolution

        self.__generate_point_list()

    def __generate_point_list(self):
        self.point_list = list()
        for x in range(self.X_lowerbound, self.X_uperbound, self.X_resolution):
            for y in range(self.Y_lowerbound, self.Y_uperbound, self.Y_resolution):
                self.point_list.append(Point(x, y))

    def generate_triangle_list(self, quantity):
        tripoint_combinations = list(itertools.combinations(self.point_list, 3))
        chosen_combinations = random.sample(tripoint_combinations, quantity)
        triangle_list = list()
        for tripoint in chosen_combinations:
            A = tripoint[0]
            B = tripoint[1]
            C = tripoint[2]
            triangle = Triangle(A, B, C)
            if triangle.is_real_triangle():
                triangle_list.append(triangle)

        return triangle_list





