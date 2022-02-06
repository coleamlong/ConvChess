class Layer:
    def __init__(self, input_shape) -> None:
        self.input_shape = input_shape
        self.input = None
        self.output = None

    # computes the output Y of a layer for a given input X
    def forward(self, input_data):
        raise NotImplementedError

    # computes dE/dX for a given dE/dY (and update parameters if any)
    def backward(self, output_error, learning_rate):
        raise NotImplementedError
