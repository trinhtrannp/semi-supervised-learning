import numpy

from src.algorithms.perceptronbased import PLAAlgorithm
from src.generators.ConvexGenerator import ConvexGenerator
from src.utils import geometry as geo_utils


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


def main(rhombus, normal):
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

    ############################# Supervised Learning #####################################

    algorithm_sp = PLAAlgorithm()

    """
    train with all training data -> this is supervised learning
    """
    labeled_training_data = get_labeled_training_data(training_rhombus_convex, training_normal_convex)
    algorithm_sp.train(classified_feature_list=labeled_training_data)

    """
    predict with test data -> supervised learning
    """
    error = 0
    for convex in test_rhombus_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        predicted_label = algorithm_sp.run(feature_vector)
        if predicted_label == -1:  # it is miss-classified
            error += 1

    for convex in test_normal_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        predicted_label = algorithm_sp.run(feature_vector)
        if predicted_label == 1:  # it is miss-classified
            error += 1

    print "error sp = ", error

    ###################################  Semi-supervised Learning  ##########################################

    algorithm_ssp = PLAAlgorithm()

    """
    train with labeled training data
    """
    labeled_training_data = get_labeled_training_data(tobe_labeled_rhombus, tobe_labeled_normal)
    algorithm_ssp.train(classified_feature_list=labeled_training_data)

    """
    pseudo-label remaining training data
    """
    pseudo_label_error = 0
    for convex in tobe_pseudo_labeled_rhombus:
        feature_vector = [convex.r1, convex.r2, convex.r3]
        predicted_label = algorithm_ssp.run(numpy.append(numpy.array(feature_vector), 1.0))
        labeled_training_data.append((predicted_label, feature_vector))
        if predicted_label == -1:
            pseudo_label_error += 1

    for convex in tobe_pseudo_labeled_normal:
        feature_vector = [convex.r1, convex.r2, convex.r3]
        predicted_label = algorithm_ssp.run(numpy.append(numpy.array(feature_vector), 1.0))
        labeled_training_data.append((predicted_label, feature_vector))
        if predicted_label == 1:
            pseudo_label_error += 1
    print "pseudo-label error = ", pseudo_label_error


    """
    re-train with new training data -> this is semi-supervised learning
    """
    algorithm_ssp.train(classified_feature_list=labeled_training_data)

    """
    predict with test data -> semi-supervised
    """
    error = 0
    for convex in test_rhombus_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        predicted_label = algorithm_ssp.run(feature_vector)
        if predicted_label == -1:  # it is miss-classified
            error += 1

    for convex in test_normal_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        predicted_label = algorithm_ssp.run(feature_vector)
        if predicted_label == 1:  # it is miss-classified
            error += 1

    print "error ssp = ", error


if __name__ == "__main__":
    main(9, 900 - 9)
