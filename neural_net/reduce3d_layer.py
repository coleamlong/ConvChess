from layer import Layer
import numpy as np


# inherit from base class Layer
class Reduce3DLayer(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self, input_size, output_size) -> None:
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.weights = np.random.rand(input_size[2]) - 0.5
        self.bias = np.random.rand(output_size[0], output_size[1])

    # returns output for a given input
    def forward(self, input_data):
        self.input = input_data
        self.output = []
        for i in range(self.input_size[0]):
            for j in range(self.input_size[1]):
                self.output[i][j] = np.dot(
                    self.input[i][j], self.weights) + self.bias[i][j]

        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)
        bias_error = np.dot(self.input.T,)

        # update parameters
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error
        return input_error
