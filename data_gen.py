import numpy as np

import chess
from stockfish import Stockfish
import random


def search(board: chess.Board, branch_count: int) -> None:
    # print(f"Branch Count: {branch_count} \n{board}")
    if branch_count == 0:
        return

    moves = []
    for legal_move in board.legal_moves:
        moves.append(legal_move)

    for i in range(branch_count):
        move_index = random.randint(0, len(moves) - 1)
        move = moves[move_index]
        new_board = board.copy()
        new_board.push(move)
        # print(f"Move: {move}\n{new_board}")

        # write new board to file
        save_file = open("fen_data.txt", "a")
        save_file.write(new_board.fen() + "\n")
        save_file.close()

        if new_board.legal_moves.count() == 0 or new_board.is_stalemate() or new_board.is_checkmate() or new_board.is_insufficient_material():
            return

        search(new_board, int(np.floor(branch_count / 2)))


board = chess.Board()
search(board, board.legal_moves.count())

iterations = 5
for i in range(iterations):
    lines = open('fen_data.txt').read().splitlines()
    myline = random.choice(lines)
    postion_fen = myline.split()[0]
    board.set_board_fen(postion_fen)
    search(board, board.legal_moves.count())
