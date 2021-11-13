import numpy as np


# loss function and its derivative
def mse(y_actual, y_estimated):
    return np.mean(np.power(y_actual - y_estimated, 2))


def mse_prime(y_actual, y_estimated):
    return 2 * (y_estimated - y_actual) / y_actual.size
