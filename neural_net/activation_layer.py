"""
Layer for handling activation functions.
"""

from neural_net.layer import Layer

__author__ = "Cole Amlong"
__credits__ = ["Omar Aflak"]


# inherit from base class Layer
class ActivationLayer(Layer):
    """
    Layer for handling activation functions
    """
    def __init__(self, activation, activation_prime) -> None:
        """
        Initialize activation layer
        :param activation: activation function
        :param activation_prime: first derivative of the activation function
        """
        super().__init__(None)
        self.activation = activation
        self.activation_prime = activation_prime

    # returns the activated input
    def forward(self, input_data):
        """
        Activate input data using activation function
        :param input_data: output data from the last layer of the network
        :return: activated input
        """
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    # returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward(self, output_error, learning_rate):
        """
        Deactivate the output error using the first
        derivative of the activation function
        :param output_error: backwards propagated error from the loss function
        :param learning_rate: scalar multiple to temper fitting
        :return: deactivated tensor for back propagation
        """
        return self.activation_prime(self.input) * output_error
