from generators.TriangleGenerator import TriangleGenerator
from utils import geometry as geo_utils


def generate_data(expected_isosceles_number, sample_quantity, increase_step):
    isosceles_triangles = list()
    normal_triangles = list()
    while len(isosceles_triangles) != expected_isosceles_number:
        del isosceles_triangles[:]
        del normal_triangles[:]
        generator = TriangleGenerator(0, 10, 0, 10, 1, 1)
        triangle_list = generator.generate_triangle_list(sample_quantity)
        for triangle in triangle_list:
            if geo_utils.is_isosceles_triangle(triangle):
                isosceles_triangles.append(triangle)
            else:
                normal_triangles.append(triangle)
        sample_quantity += increase_step

    return isosceles_triangles, normal_triangles


def main():
    print "Trying to generate 100 isosceles triangle..."
    isosceles_triangles, normal_triangles = generate_data(100, 5000, 100)

    print "Sample labeled data"



if __name__ == "__main__":
    main()
