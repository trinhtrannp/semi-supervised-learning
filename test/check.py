import matplotlib.pyplot as plt
from generator.TriangleGenerator import TriangleGenerator

plt.figure()
plt.axes(xlim=(0, 5), ylim=(0, 5))
patch = plt.Circle((5, -5), 0.75, fc='y')


def main():
    generator = TriangleGenerator(0, 5, 0, 5, 1, 1)
    triangle_list = generator.generate_triangle_list(3)

    plt.gca().add_patch(patch)
    plt.show()


if __name__ == "__main__":
    main()
