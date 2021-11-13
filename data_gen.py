import numpy as np

import chess
from stockfish import Stockfish
import random

board_fens = set()


def search(board: chess.Board, branch_count: int) -> None:
    if branch_count == 0:
        return

    moves = []
    for legal_move in board.legal_moves:
        moves.append(legal_move)

    for i in range(branch_count):
        # make a random move
        move = random.choice(moves)
        new_board = board.copy()
        new_board.push(move)

        # append new board to set
        board_fens.add(new_board.fen())

        # branch end conditions
        if new_board.legal_moves.count() == 0 or new_board.is_stalemate() or new_board.is_checkmate() or new_board.is_insufficient_material():
            return

        # recursive step
        search(new_board, int(branch_count / 4))


def evaluate(fens: str, stockfish) -> None:
    lines_to_write = []
    for fen in fens:
        stockfish.set_fen_position(fen)
        data_line = [str(stockfish.get_evaluation()["value"]), fen]
        lines_to_write.append(" ".join(data_line))
        print(f"Evaluated FEN: {fen}")
    data_file = open("data.txt", "a")
    data_file.write("\n".join(lines_to_write))
    data_file.close()


# # initial search
board = chess.Board()
search(board, board.legal_moves.count())

iterations = 10
for i in range(iterations):
    # choose a random visited postion from file
    my_fen = random.choice(list(board_fens))
    print(f"Looking at {my_fen}")
    my_fen_position = my_fen.split()[0]
    # search again from chosen position
    board.set_board_fen(my_fen_position)
    search(board, board.legal_moves.count())

stockfish = Stockfish("stockfish.exe")
stockfish.set_depth(2)
evaluate(board_fens, stockfish)
