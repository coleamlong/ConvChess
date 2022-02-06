from neural_net.layer import Layer
import numpy as np


# inherit from base class Layer
class MaxPoolLayer(Layer):
    # input_dim = number of input neurons
    # filter_dim = number of output neurons
    def __init__(self, input_shape, kernel_size, stride) -> None:
        super().__init__(input_shape)
        self.kernel_size = kernel_size
        self.stride = stride

        # out_dim = input_dim - filter_dim + 1
        self.out_dim = tuple(map(int, tuple(np.floor(np.subtract(input_shape, kernel_size) / stride) + 1)))

    # returns output for a given input
    def forward(self, input_data):
        self.input = input_data
        self.output = np.zeros(self.out_dim)
        curr_y = 0

        for j in range(self.out_dim[1]):
            curr_x = 0

            for i in range(self.out_dim[0]):
                window = input_data[curr_x:curr_x + self.kernel_size][0][curr_y:curr_y + self.kernel_size]
                self.output[i][j] = np.max(window)
                curr_x += self.stride

            curr_y += self.stride

        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward(self, output_error, learning_rate):
        return output_error
