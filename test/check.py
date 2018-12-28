import math
import random

import matplotlib.pyplot as plt
from plotly.utils import numpy

from generator.TriangleGenerator import TriangleGenerator
from model.Angle import Angle

plt.figure()
plt.axes(xlim=(0, 5), ylim=(0, 5))


def main():
    generator = TriangleGenerator(0, 5, 0, 5, 1, 1)
    triangle_list = generator.generate_triangle_list(10)

    for triangle in triangle_list:
        tp = plt.Polygon(xy=triangle.to_xy_list(), color=[random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)])
        plt.gca().add_patch(tp)

    plt.show()


if __name__ == "__main__":
    main()
