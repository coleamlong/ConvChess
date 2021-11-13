import numpy as np


# binary step
def bin_step(x):
    return 0 if x < 0 else 1


def bin_step_prime(x):
    raise NotImplementedError


# ReLU
def relu(x):
    return max(0, x)


def relu_prime(x):
    raise NotImplementedError


# Linear
def linear(x):
    return x


def linear_prime(x):
    return 1


# Tanh
def tanh(x):
    return np.tanh(x)


def tanh_prime(x):
    return 1 - np.tanh(x)**2


# Softmax
def softmax(x):
    raise NotImplementedError


def softmax_prime(x):
    raise NotImplementedError


# Sigmoid
def sigmoid(x):
    raise NotImplementedError


def sigmoid_prime(x):
    raise NotImplementedError
