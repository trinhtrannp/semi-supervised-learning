import numpy
import matplotlib.pyplot as plt

from src.algorithms.perceptronbased import PLAAlgorithm
from src.generators.ConvexGenerator import ConvexGenerator
from src.utils import geometry as geo_utils


def generate_rhombus_convex(expected_number, sample_quantity, increase_step):
    rhombus_convex = list()
    generator = ConvexGenerator(0, 10, 0, 10, 1, 1)
    while len(rhombus_convex) != expected_number:
        del rhombus_convex[:]
        convex_list = generator.generate_convex_list(sample_quantity)
        for convex in convex_list:
            if geo_utils.is_rhombus_convex(convex):
                rhombus_convex.append(convex)
                if len(rhombus_convex) >= expected_number:
                    break

        sample_quantity += increase_step
        del convex_list[:]

    return rhombus_convex


def generate_normal_convex(expected_number, sample_quantity, increase_step):
    normal_convex = list()
    generator = ConvexGenerator(0, 10, 0, 10, 1, 1)
    while len(normal_convex) != expected_number:
        del normal_convex[:]
        convex_list = generator.generate_convex_list(sample_quantity)
        for convex in convex_list:
            if not geo_utils.is_rhombus_convex(convex):
                normal_convex.append(convex)
                if len(normal_convex) >= expected_number:
                    break

        sample_quantity += increase_step
        del convex_list[:]

    return normal_convex


def get_labeled_training_data(tobe_labeled_rhombus, tobe_labeled_normal):
    labeled_training_data = list()
    for convex in tobe_labeled_rhombus:
        labeled_training_data.append((1, [convex.r1, convex.r2, convex.r3]))

    for convex in tobe_labeled_normal:
        labeled_training_data.append((-1, [convex.r1, convex.r2, convex.r3]))

    return labeled_training_data


def main(rhombus, normal):
    #print "Trying to generate ", rhombus, " rhombus convex..."
    rhombus_convex = generate_rhombus_convex(rhombus, 10000, 1000)

    #print "Trying to generate ", normal, " normal convex..."
    normal_convex = generate_normal_convex(normal, 10000, 1000)

    """
    divide into three parts.
    one-third will be used as training data
    two-third will be used as test data
    """
    training_rhombus_convex = rhombus_convex[:int((len(rhombus_convex) * 0.2))]
    test_rhombus_convex = rhombus_convex[int((len(rhombus_convex) * 0.8)):]
    del rhombus_convex[:]

    training_normal_convex = normal_convex[:int((len(normal_convex) * 0.01))]
    test_normal_convex = normal_convex[int((len(normal_convex) * 0.99)):]
    del normal_convex[:]

    """
    take one-third training data to label
    the remaining two-third will be pseudo-labeled
    """
    tobe_labeled_rhombus = training_rhombus_convex[:int((len(training_rhombus_convex)*0.5))]
    tobe_pseudo_labeled_rhombus = training_rhombus_convex[int((len(training_rhombus_convex)*0.5)):]
    del training_rhombus_convex[:]

    tobe_labeled_normal = training_normal_convex[:int((len(training_normal_convex)*0.1))]
    tobe_pseudo_labeled_normal = training_normal_convex[int((len(training_normal_convex)*0.9)):]
    del training_normal_convex[:]

    ############################# Supervised Learning #####################################

    algorithm_sp = PLAAlgorithm()

    """
    train with all training data -> this is supervised learning
    """
    labeled_training_data = get_labeled_training_data(tobe_labeled_rhombus, tobe_labeled_normal)
    loss_record = algorithm_sp.train(classified_feature_list=labeled_training_data)
    # plt.figure(1)
    # plt.xlabel('iterations')
    # plt.ylabel('#of miss-classified')
    # plt.plot(list(range(0, len(loss_record))), loss_record, '*-')
    # plt.show()

    """
    predict with test data -> supervised learning
    """
    error = 0
    for convex in test_rhombus_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        value, predicted_label = algorithm_sp.run(feature_vector)
        if predicted_label == -1:  # it is miss-classified
            error += 1

    for convex in test_normal_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        value, predicted_label = algorithm_sp.run(feature_vector)
        if predicted_label == 1:  # it is miss-classified
            error += 1

    sp_error = error

    ###################################  Semi-supervised Learning  ##########################################

    algorithm_ssp = PLAAlgorithm()

    """
    train with labeled training data
    """
    labeled_training_data = get_labeled_training_data(tobe_labeled_rhombus, tobe_labeled_normal)
    loss_record = algorithm_ssp.train(classified_feature_list=labeled_training_data)

    """
    pseudo-label remaining training data
    """
    pseudo_label_error = 0
    pseudo_rhombus_data = list()
    for convex in tobe_pseudo_labeled_rhombus:
        feature_vector = [convex.r1, convex.r2, convex.r3]
        value, predicted_label = algorithm_ssp.run(numpy.append(numpy.array(feature_vector), 1.0))
        pseudo_rhombus_data.append((value, feature_vector))
        if predicted_label == -1:
            pseudo_label_error += 1

    pseudo_rhombus_data.sort(key=lambda item: item[0], reverse=True)

    pseudo_normal_data = list()
    for convex in tobe_pseudo_labeled_normal:
        feature_vector = [convex.r1, convex.r2, convex.r3]
        value, predicted_label = algorithm_ssp.run(numpy.append(numpy.array(feature_vector), 1.0))
        pseudo_normal_data.append((value, feature_vector))
        if predicted_label == 1:
            pseudo_label_error += 1

    pseudo_normal_data.sort(key=lambda item: item[0])

    pseudo_rhombus_data = pseudo_rhombus_data[:int(len(pseudo_rhombus_data) * 1.0)]
    pseudo_normal_data = pseudo_normal_data[:int(len(pseudo_normal_data) * 1.0)]
    for i in range(0, max(len(pseudo_rhombus_data), len(pseudo_normal_data))):
        if len(pseudo_normal_data) > i:
            labeled_training_data.append((-1, pseudo_normal_data[i][1]))

        if len(pseudo_rhombus_data) > i:
            labeled_training_data.append((1, pseudo_rhombus_data[i][1]))

    #print "pseudo-label error = ", pseudo_label_error


    """
    re-train with new training data -> this is semi-supervised learning
    """
    algorithm_ssp = PLAAlgorithm()
    loss_record = algorithm_ssp.train(classified_feature_list=labeled_training_data)
    # plt.figure(2)
    # plt.xlabel('iterations')
    # plt.ylabel('#of miss-classified')
    # plt.plot(list(range(0, len(loss_record))), loss_record, '*-')
    # plt.show()

    """
    predict with test data -> semi-supervised
    """
    error = 0
    for convex in test_rhombus_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        value, predicted_label = algorithm_ssp.run(feature_vector)
        if predicted_label == -1:  # it is miss-classified
            error += 1

    for convex in test_normal_convex:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        value, predicted_label = algorithm_ssp.run(feature_vector)
        if predicted_label == 1:  # it is miss-classified
            error += 1

    ssp_error = error

    return sp_error, ssp_error


def predict_with_data(model, data_set, expected_label):
    error = 0
    labeled_data = list()
    for convex in data_set:
        feature_vector = numpy.array([convex.r1, convex.r2, convex.r3, 1.0])
        value, predicted_label = model.run(feature_vector)
        labeled_data.append((predicted_label, feature_vector))
        if predicted_label != expected_label:  # it is miss-classified
            error += 1

    return error, labeled_data


if __name__ == "__main__":
    sp_errors = []
    ssp_errors = []
    for i in range(0, 20):
        print i
        sp_error, ssp_error = main(30, 10000 - 30)
        sp_errors.append(sp_error)
        ssp_errors.append(ssp_error)
        print ""

    sp_errors = numpy.array(sp_errors)
    sp_errors_mean = [sp_errors.mean()]*len(sp_errors)

    ssp_errors = numpy.array(ssp_errors)
    ssp_errors_mean = [ssp_errors.mean()]*len(ssp_errors)

    plt.figure(1)
    plt.xlabel('#of try')
    plt.ylabel('#of miss-classified')
    plt.plot(list(range(0, len(sp_errors))), sp_errors, 'r*-',
             list(range(0, len(ssp_errors))), ssp_errors, '*-',
             list(range(0, len(sp_errors))), sp_errors_mean, 'r--',
             list(range(0, len(ssp_errors))), ssp_errors_mean, '--',
             )
    plt.legend(("SL", "SSL"))

    plt.show()
