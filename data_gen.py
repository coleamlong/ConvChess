import chess
import chess.engine
import random
import numpy as np
from os.path import exists

STOCKFISH_PATH = "stockfish.exe"

FENS_PATH = "data/fens.txt"
SCORES_PATH = "data/scores.txt"


def random_board(max_depth=200) -> chess.Board:
    board = chess.Board()
    depth = random.randrange(0, max_depth)

    for _ in range(depth):
        all_moves_from_pos = list(board.legal_moves)
        random_move = random.choice(all_moves_from_pos)
        board.push(random_move)
        if board.is_game_over():
            break

    return board


def evaluate(board, engine_depth):
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as sf:
        result = sf.analyse(board, chess.engine.Limit(depth=engine_depth))
        score = result["score"].white().score()
        return score


def get_square_indices(square: chess.Square):
    return chess.square_file(square), chess.square_rank(square)


def to_matrix(board: chess.Board):
    board_matrix = np.zeros((14, 8, 8), dtype=np.int8)

    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = np.unravel_index(square, (8, 8))
            board_matrix[piece - 1][7 - idx[0]][idx[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            idx = np.unravel_index(square, (8, 8))
            board_matrix[piece + 5][7 - idx[0]][idx[1]] = 1

    temp = board.turn

    board.turn = chess.WHITE
    for move in board.legal_moves:
        i, j = get_square_indices(move.to_square)
        board_matrix[12][i][j] = 1

    board.turn = chess.BLACK
    for move in board.legal_moves:
        i, j = get_square_indices(move.to_square)
        board_matrix[13][i][j] = 1

    board.turn = temp

    return board_matrix


def generate_data(count: int, board_depth=200, engine_depth=10):
    boards = []
    scores = []

    for i in range(count):
        board = random_board(board_depth)
        score = evaluate(board, engine_depth)
        boards.append(board)
        scores.append(score)
        if i % 10 == 0:
            if i % 100 == 0:
                print()
            print(".", end="")

    boards = np.asarray(boards)
    scores = np.asarray(scores, dtype=np.float32)
    nan_indicies = np.argwhere(np.isnan(scores))
    boards = np.delete(boards, nan_indicies)
    scores = np.delete(scores, nan_indicies)

    board_mats = []
    for board in boards:
        board_mats.append(to_matrix(board))

    board_mats = np.asarray(board_mats, dtype=np.float32)
    return board_mats, scores


def pull_data():
    if not exists(FENS_PATH) or not exists(SCORES_PATH):
        return

    with open(FENS_PATH) as fens_text:
        board_fens = np.loadtxt(fens_text, dtype=str)

    board_mats = []

    for fen in board_fens:
        board = chess.Board()
        board.set_board_fen(fen[0])
        board_mats.append(to_matrix(board))

    with open(SCORES_PATH, "w+") as scores_txt:
        scores = np.loadtxt(scores_txt)



    return board_mats, scores

