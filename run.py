import numpy

from algorithms.perceptronbased import PLAAlgorithm
from generators.ConvexGenerator import ConvexGenerator
from utils import geometry as geo_utils


def generate_rhombus_convex(expected_number, sample_quantity, increase_step):
    rhombus_convex = list()
    while len(rhombus_convex) != expected_number:
        del rhombus_convex[:]
        generator = ConvexGenerator(0, 10, 0, 10, 1, 1)
        convex_list = generator.generate_convex_list(sample_quantity)
        for convex in convex_list:
            if geo_utils.is_rhombus_convex(convex):
                rhombus_convex.append(convex)
                if len(rhombus_convex) == expected_number:
                    break
        sample_quantity += increase_step

    return rhombus_convex


def generate_normal_convex(expected_number, sample_quantity, increase_step):
    normal_convex = list()
    while len(normal_convex) != expected_number:
        del normal_convex[:]
        generator = ConvexGenerator(0, 10, 0, 10, 1, 1)
        convex_list = generator.generate_convex_list(sample_quantity)
        for convex in convex_list:
            if not geo_utils.is_rhombus_convex(convex):
                normal_convex.append(convex)
                if len(normal_convex) == expected_number:
                    break

        sample_quantity += increase_step

    return normal_convex


def get_labeled_training_data(tobe_labeled_rhombus, tobe_labeled_normal):
    labeled_training_data = list()
    for convex in tobe_labeled_rhombus:
        labeled_training_data.append((1, [convex.r1, convex.r2, convex.r3]))

    for convex in tobe_labeled_normal:
        labeled_training_data.append((-1, [convex.r1, convex.r2, convex.r3]))

    return labeled_training_data


def main(algorithm, rhombus, normal):
    print "Trying to generate ", rhombus, " rhombus convex..."
    rhombus_convex = generate_rhombus_convex(rhombus, 10000, 1000)

    print "Trying to generate ", normal, " normal convex..."
    normal_convex = generate_normal_convex(normal, 10000, 1000)

    """
    divide into three parts.
    one-third will be used as training data
    two-third will be used as test data
    """
    training_rhombus_convex = rhombus_convex[:len(rhombus_convex) // 3]
    test_rhombus_convex = rhombus_convex[len(rhombus_convex) // 3:]

    training_normal_convex = normal_convex[:len(normal_convex) // 3]
    test_normal_convex = normal_convex[len(normal_convex) // 3:]

    """
    take one-third training data to label
    the remaining two-third will be pseudo-labeled
    """
    tobe_labeled_rhombus = training_rhombus_convex[:len(training_rhombus_convex) // 3]
    tobe_pseudo_labeled_rhombus = training_rhombus_convex[len(training_rhombus_convex) // 3:]

    tobe_labeled_normal = training_normal_convex[:len(training_normal_convex) // 3]
    tobe_pseudo_labeled_normal = training_normal_convex[len(training_normal_convex) // 3:]

    """
    train with labeled data -> this is supervised learning
    """
    labeled_training_data = get_labeled_training_data(tobe_labeled_rhombus, tobe_labeled_normal)
    algorithm.train(classified_feature_list=labeled_training_data)

    """
    predict with test data
    """
    loss = 0
    for convex in test_rhombus_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        predicted_label = algorithm.run(feature_vector)
        if predicted_label == -1:  # it is miss-classified
            loss += 1

    for convex in test_normal_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        predicted_label = algorithm.run(feature_vector)
        if predicted_label == 1:  # it is miss-classified
            loss += 1

    print "loss = ", loss


if __name__ == "__main__":
    algorithm = PLAAlgorithm()
    main(algorithm, 9, 900 - 9)
