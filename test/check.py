import math
import random

import matplotlib.pyplot as plt
from plotly.utils import numpy

from generators.TriangleGenerator import TriangleGenerator
from models.Angle import Angle


def test_triangle_generator():
    plt.figure()
    plt.axes(xlim=(0, 5), ylim=(0, 5))

    generator = TriangleGenerator(0, 5, 0, 5, 1, 1)
    triangle_list = generator.generate_triangle_list(10)

    for triangle in triangle_list:
        tp = plt.Polygon(xy=triangle.to_numpy_array(),
                         color=[random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)])
        plt.gca().add_patch(tp)

    plt.show()


def test_numpy_array():
    x1 = numpy.arange(3.0)
    x2 = numpy.arange(3.0)
    y = numpy.add(x1, x2)
    z = numpy.add(x1, 0.5)

    print y, z


def test_python_dict():
    a = [1.3, 2.8, 3.0, 5]
    b = a[:2]
    print b

    b = a[2:]
    print b


def main():
    test_python_dict()


if __name__ == "__main__":
    main()
