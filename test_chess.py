import numpy as np
import chess
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

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

x_train = x_data[0:len(x_data) - 11]
y_train = y_data[0:len(y_data) - 11]
x_test = x_data[len(x_data) - 10:len(x_data) - 1]
y_test = y_data[len(y_data) - 10:len(y_data) - 1]
print(chess.PIECE_TYPES)



