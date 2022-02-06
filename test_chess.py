import numpy as np

from neural_net.network import Network
from neural_net.fc_layer import FCLayer
from neural_net.convolutional_layer import ConvLayer
from neural_net.max_pooling_layer import MaxPoolLayer
from neural_net.activation_layer import ActivationLayer
from neural_net.activation_functions import tanh, tanh_prime, linear, linear_prime
from neural_net.loss_functions import mse, mse_prime

import chess

chess_dict = {
    "p": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "P": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    "n": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "N": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "b": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "B": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    "r": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "R": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "q": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    "Q": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "k": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    "K": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    "None": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}


def to_matrix(fen: str):
    board_matrix = []
    board = chess.Board(fen)
    for rank in chess.RANK_NAMES:
        board_rank = []
        for file in chess.FILE_NAMES:
            piece = board.piece_at(chess.parse_square(file + rank))
            if piece:
                board_rank.append(chess_dict[piece.symbol()])
            else:
                board_rank.append(chess_dict["None"])
        board_matrix.append(board_rank)
    return board_matrix


with open("fens.csv") as fens_csv:
    x_data_raw = np.loadtxt(fens_csv, dtype=str, delimiter=",")
x_data = list(map(to_matrix, x_data_raw))

with open("evals.csv") as evals_csv:
    y_data = np.loadtxt(evals_csv, delimiter=",")

print(x_data[0], y_data[0])

x_train = x_data[0:len(x_data) - 11]
y_train = y_data[0:len(y_data) - 11]
x_test = x_data[len(x_data) - 10:len(x_data) - 1]
y_test = y_data[len(y_data) - 10:len(y_data) - 1]

# network
net = Network()
net.add(ConvLayer((8, 8, 12), (1, 1, 12)))
net.add(MaxPoolLayer((8, 8), 2, 2))
net.add(FCLayer(16, 8))
net.add(ActivationLayer(tanh, tanh_prime))
net.add(FCLayer(8, 1))
net.add(ActivationLayer(linear, linear_prime))

# train
net.use(mse, mse_prime)
net.fit(x_train, y_train, epochs=30, learning_rate=0.1)

output = net.predict(x_test)
error = np.mean(output != y_test)
print(f"Error = {error}%")
