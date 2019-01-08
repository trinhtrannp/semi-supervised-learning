import math
import numpy


def is_isosceles_triangle(triangle):
    # return triangle.a == triangle.b or triangle.a == triangle.c or triangle.b == triangle.c
    return triangle.a == triangle.b == triangle.c


def is_rhombus_convex(convex):
    tolerance = 0.1
    if abs(convex.ab - convex.bc) > tolerance:
        return False

    if abs(convex.bc - convex.cd) > tolerance:
        return False

    if abs(convex.cd - convex.da) > tolerance:
        return False

    return True


def clean_cos(cos_value):
    return min(1, max(cos_value, -1))


def vector_angle_def(vecA, vecB):
    math.degrees(vector_angle_rad(vecA, vecB))


def vector_angle_rad(vecA, vecB):
    vecAnp = numpy.array(vecA)
    vecBnp = numpy.array(vecB)
    angle_radian = math.acos(
        clean_cos((numpy.dot(vecAnp, vecBnp)) / (numpy.linalg.norm(vecAnp) * numpy.linalg.norm(vecBnp))))
    return angle_radian


def point_angle_deg(A, B, C):
    """

    :param A: Point A
    :param B: Point B
    :param C: Point C
    :return: angle in degree between two vector AB and vector AC
    """
    return math.degrees(point_angle_rad(A, B, C))


def point_angle_rad(A, B, C):
    """

    :param A: Point A
    :param B: Point B
    :param C: Point C
    :return: angle in radian between two vector AB and vector AC
    """
    vecAB = [B.x - A.x, B.y - A.y]
    vecAC = [C.x - A.x, C.y - A.y]
    return vector_angle_rad(vecAB, vecAC)
