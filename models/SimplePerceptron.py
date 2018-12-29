from plotly.utils import numpy


class SimplePerceptron(object):

    def __init__(self, activation_function):
        if activation_function is None:
            raise Exception('activation_function cannot be null')

        self.activation_function = activation_function

    def get_output(self, weight=None, feature_vector=None):
        value = numpy.dot(weight.T, feature_vector)
        return self.activation_function.calc(input_value=value)
