import itertools
import random

from src.models.Point import Point
from src.models import Convex


class ConvexGenerator(object):

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

    def generate_convex_list(self, quantity):
        quadpoint_combinations = list(itertools.combinations(self.point_list, 4))
        chosen_combinations = random.sample(quadpoint_combinations, quantity)
        convex_list = list()
        for quadpoint in chosen_combinations:
            point1 = quadpoint[0]
            point2 = quadpoint[1]
            point3 = quadpoint[2]
            point4 = quadpoint[3]
            convex = Convex(point1, point2, point3, point4)
            if convex.is_real_convex():
                convex_list.append(convex)

        return convex_list
