import numpy as np

from network import Network
from fc_layer import FCLayer
from activation_layer import ActivationLayer
from activation_functions import tanh, tanh_prime, linear, linear_prime
from loss_functions import mse, mse_prime

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


x_data = []
y_data = []
data_lines = open("data.txt").read().splitlines()
for line in data_lines:
    line_array = line.split(" ", 1)
    y_data.append(line_array[0])
    x_data.append(to_matrix(line_array[1]))

x_train = x_data[0:len(x_data) - 11]
y_train = y_data[0:len(y_data) - 11]
x_test = x_data[len(x_data) - 10:len(x_data) - 1]
y_test = y_data[len(y_data) - 10:len(y_data) - 1]

# network
net = Network()
net.add(FCLayer(64, 10))
net.add(ActivationLayer(tanh, tanh_prime))
net.add(FCLayer(10, 10))
net.add(ActivationLayer(tanh, tanh_prime))
net.add(FCLayer(10, 1))
net.add(ActivationLayer(linear, linear_prime))

# train
net.use(mse, mse_prime)
net.fit(x_train, y_train, epochs=30, learning_rate=0.1)

output = net.predict(x_test)
error = np.mean(output != y_test)
print(f"Error = {error}%")
