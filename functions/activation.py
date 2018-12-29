class BaseActivationFunction(object):
    def calc(self, input_value):
        pass


class SignumActivationFunction(BaseActivationFunction):

    def calc(self, input_value):
        if input >= 0:
            return 1
        else:
            return -1
