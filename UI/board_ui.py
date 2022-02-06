import chess
from tkinter import *


class BoardUI:
    def __init__(self):
        self.fen = chess.STARTING_FEN

        self.board_buttons =  [len(chess.RANK_NAMES)][len(chess.FILE_NAMES)]
        for rank in self.board_buttons:



    def refresh
