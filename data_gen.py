import numpy as np

import chess
from stockfish import Stockfish
import random

fens = set()


def search(current_board: chess.Board, branch_count: int, decay_rate=0.25) -> None:
    if branch_count == 0:
        return

    moves = []
    for legal_move in current_board.legal_moves:
        moves.append(legal_move)

    for i in range(branch_count):
        # make a random move
        move = random.choice(moves)
        new_board = current_board.copy()
        new_board.push(move)

        # append new board to set
        fens.add(new_board.fen())

        # branch end conditions
        if new_board.legal_moves.count() == 0 or \
                new_board.is_stalemate() or \
                new_board.is_checkmate() or \
                new_board.is_insufficient_material():
            return

        # recursive step
        search(new_board, int(branch_count * decay_rate), decay_rate)


def evaluate(fens: str, engine) -> None:
    evals = []
    for fen in fens:
        engine.set_fen_position(fen)
        board_eval = engine.get_evaluation()["value"]
        evals.append(board_eval)

    np.savetxt("evals.csv", evals, fmt="%s", delimiter=",")


# # initial search
board = chess.Board()
search(board, board.legal_moves.count())

iterations = 10
for i in range(iterations):
    # choose a random visited position from file
    my_fen = np.random.choice(list(fens))
    my_fen_position = my_fen.split()[0]
    # search again from chosen position
    board.set_board_fen(my_fen_position)
    search(board, board.legal_moves.count())

engine = Stockfish("stockfish.exe")
engine.set_depth(2)
np.savetxt("fens.csv", list(fens), fmt="%s", delimiter=",")
evaluate(fens, engine)
