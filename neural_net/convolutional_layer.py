from neural_net.layer import Layer
import numpy as np


# inherit from base class Layer
class ConvLayer(Layer):
    # input_dim = number of input neurons
    # filter_dim = number of output neurons
    def __init__(self, input_shape, filter_dim) -> None:
        super().__init__(input_shape)
        self.weights = np.random.rand(*filter_dim)
        # out_dim = input_dim - filter_dim + 1
        self.out_dim = tuple(np.subtract(input_shape, filter_dim) + 1)
        self.bias = np.random.rand(*self.out_dim) - 0.5

    # returns output for a given input
    def forward(self, input_data):
        self.input = input_data
        self.output = np.zeros(self.out_dim)
   
        for j in range(self.out_dim[1]):
            for i in range(self.out_dim[0]):
                self.output[i][j] = sum(self.input[i][j] * self.weights[0][0]) 
        
        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward(self, output_error, learning_rate):
        input_error = np.dot(output_error, np.average(self.weights.T))

        avg = np.average(output_error)
        self.weights -= learning_rate * avg
        for j in range(self.out_dim[1]):
            for i in range(self.out_dim[0]):
                self.bias[i][j] -= learning_rate * output_error[i][j]

        return input_error
