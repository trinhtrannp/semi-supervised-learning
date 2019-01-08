from src.algorithms.BaseAlgorithm import BaseAlgorithm
from src.functions.activation import SignumActivationFunction
from src.models.SimplePerceptron import SimplePerceptron
import numpy


class PLAAlgorithm(BaseAlgorithm):
    def __init__(self, activation_function=SignumActivationFunction(), initial_weight=None):
        self.weight = initial_weight
        self.activation_function = activation_function
        self.perceptron = SimplePerceptron(activation_function=activation_function)

    def init_weight(self, feature_vector_length):
        if self.weight is None:
            self.weight = numpy.zeros(feature_vector_length)
            self.weight = numpy.add(self.weight, 0.01)

    def train(self, classified_feature_list, expected_loss=0):
        self.classified_feature_list = classified_feature_list
        while True:
            loss = 0
            """TODO: randomly choose from classified feature list"""
            for feature_point in self.classified_feature_list:
                true_label = feature_point[0]
                feature_vector = numpy.append(numpy.array(feature_point[1]), 1.0)
                if self.weight is None:
                    self.init_weight(len(feature_vector))

                value, predict_label = self.run(feature_vector)
                if predict_label != true_label:
                    loss += 1
                    self.weight = numpy.add(self.weight, numpy.multiply(feature_vector, true_label))

            if loss <= expected_loss:
                break

    def run(self, feature_vector):
        """
            :return class of feature_vector
        """
        value, label = self.perceptron.get_output(self.weight, feature_vector)
        return value, label
