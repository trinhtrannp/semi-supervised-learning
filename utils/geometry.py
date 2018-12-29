def is_isosceles_triangle(triangle):
    return triangle.a == triangle.b or triangle.a == triangle.c or triangle.b == triangle.c


def clean_cos(cos_value):
    return min(1, max(cos_value, -1))
