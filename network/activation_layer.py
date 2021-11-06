from layer import Layer


# inherit from base class Layer
class ActivationLayer(Layer):
    def __init__(self, activation, activation_prime) -> None:
        super().__init__()
        self.activation = activation
        self.activation_prime = activation_prime

    # returns the activated input
    def forward(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    # returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward(self, output_error, learning_rate):
        return self.activation_prime(self.input) * output_error
