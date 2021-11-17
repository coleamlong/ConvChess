from tkinter import *
import tkinter
import chess

WIDTH, HEIGHT = 1000, 800
BOARD_COLORS = ["#444444", "#aaaaaa"]
SQUARE_SIZE = 100


class Root(Tk):
    def __init__(self, boardSize=8) -> None:
        super(Root, self).__init__()
        self.boardSize = boardSize
        self.title("ChessAI")
        self.middleframe = tkinter.Frame(self)
        self.middleframe.grid(row=8, column=8)
        self.wm_iconbitmap('window_icon.ico')
        self.resizable(False, False)

        self.canvas = tkinter.Canvas(
            self, bg="white", width=WIDTH, height=HEIGHT)
        self.canvas.grid(row=0, column=1, columnspan=8, rowspan=8)
        self.board = [[None for row in range(boardSize)]
                      for col in range(boardSize)]

    def init_board(self):
        from itertools import cycle

        for col in range(self.boardSize):

            color = cycle(BOARD_COLORS[::-1] if not col % 2 else BOARD_COLORS)
            for row in range(self.boardSize):

                self.board[row][col] = SquareButton(
                    self.canvas, row, col, SQUARE_SIZE, next(color))


class SquareButton:
    def __init__(self, canvas: tkinter.Canvas, row: int, column: int, size: int, color: str) -> None:
        self.row = row
        self.column = column
        self.size = size
        self.color = color

        x1 = self.row * self.size
        y1 = self.column * self.size
        x2 = x1 + self.size
        y2 = y1 + self.size
        canvas.create_rectangle(
            x1, y1, x2, y2, fill=self.color, tags=f"tile{self.column}{self.row}", outline="")
        canvas.tag_bind(f"tile{self.column}{self.row}",
                        "<Button-1>", self.__str__)

    def __str__(self, event=None):
        print(
            f"{chess.FILE_NAMES[self.row]}{chess.RANK_NAMES[7 - self.column]}")


# root = Root()
# root.init_board()
# root.mainloop()

board = chess.Board()
print(board)
board.push_uci("e2e4")
string =
print(string)
