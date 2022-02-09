"""
Main GUI class for Convolutional Chess Engine project
"""

from button import Button

import pygame as pg
import chess
import itertools

__author__ = "Cole Amlong"
__credits__ = ["Eddie Sharick", "Esteban Küber"]

# CONSTANTS
SCALE = 1
BOARD_WIDTH, BOARD_HEIGHT = 512 * SCALE, 512 * SCALE
EVAL_WIDTH, EVAL_HEIGHT = 32 * SCALE, BOARD_HEIGHT
MENU_WIDTH, MENU_HEIGHT = BOARD_WIDTH + EVAL_WIDTH, 128 * SCALE
MAX_FPS = 30

BG_COLOR = (63, 63, 63)
BG_COLOR_ACCENT = (127, 127, 127)

LT_SQUARE_COLOR = (255, 255, 255)
DK_SQUARE_COLOR = (215, 215, 215)

BOARD_SIZE = 8
SQ_SIZE = BOARD_WIDTH // BOARD_SIZE

IMAGES = {}


def load_images():
    """
    Initializes dictionary of chess piece images. Called exactly once in main method.
    """
    for color in chess.COLOR_NAMES:
        for piece in chess.PIECE_NAMES:
            if piece is None:
                # filter out empty square
                continue

            piece_name = f"{color}_{piece}"
            IMAGES[piece_name] = \
                pg.transform.smoothscale(pg.image.load(f"assets/pieces/{piece_name}.png"), (SQ_SIZE, SQ_SIZE))


def draw_squares(screen):
    """
    Draws a base chess board of alternating colors onto screen
    :param screen: a pygame canvas
    """
    color = itertools.cycle([pg.Color(LT_SQUARE_COLOR), pg.Color(DK_SQUARE_COLOR)])

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            pg.draw.rect(screen, next(color), pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        next(color)


def draw_pieces(screen, board: chess.Board):
    """
    Draws chess pieces for of board onto screen
    :param screen: a pygame canvas
    :param board: a chess board
    """
    for square in chess.SQUARES:
        chess_piece = board.piece_at(square)

        if chess_piece is None:
            # handle empty square
            continue

        # build images dictionary key
        piece_color = chess.COLOR_NAMES[0] if chess_piece.color else chess.COLOR_NAMES[1]
        piece_name = f"{piece_color}_{chess.piece_name(chess_piece.piece_type)}"

        row = chess.square_rank(square)
        col = chess.square_file(square)

        screen.blit(IMAGES[piece_name], pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_check(screen, board: chess.Board):
    """
    If a king is in check, highlight the king's square red
    :param screen: a pygame canvas
    :param board: a chess board
    """
    if board.is_check():
        # create highlight object
        s = pg.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(200)
        s.fill(pg.Color("red"))

        king_square = board.king(board.turn)
        screen.blit(s, (chess.square_file(king_square) * SQ_SIZE, chess.square_rank(king_square) * SQ_SIZE))


def draw_eval(screen, evaluation: int):
    """
    Draws the evaluation bar onto screen based upon the value of evaluation
    :param screen: a pygame canvas
    :param evaluation: integer representing an engine's evaluation of the current board position
    """
    pg.draw.rect(screen, pg.Color("white"),
                 pg.Rect(BOARD_WIDTH, 0, EVAL_WIDTH, EVAL_HEIGHT))
    pg.draw.rect(screen, pg.Color("black"),
                 pg.Rect(BOARD_WIDTH, 0, EVAL_WIDTH, EVAL_HEIGHT * (evaluation / 2000) + (EVAL_HEIGHT / 2)))


def draw_menu(screen, menu_components, board: chess.Board):
    """
    Draws all menu components onto screen
    :param screen: a pygame canvas
    :param menu_components: a list of objects to draw
    :param board: a chess board
    """
    for item in menu_components:
        item.draw(screen, False)


def draw_screen(screen, board: chess.Board, menu_components, selected_square, show_eval=False, evaluation=0):
    """
    Draws all elements onto screen. Includes menu, chess board, and evaluation bar
    :param screen: a pygame canvas
    :param board: a chess board:
    :param menu_components: a list of menu components, used in draw_menu()
    :param selected_square: a tuple of the indices of the last user-selected square, used for highlighting
    :param show_eval: flag controlling drawing evaluation bar
    :param evaluation: integer representing an engine's evaluation of the current board position
    """
    draw_menu(screen, menu_components, board)
    draw_board(screen, board, selected_square)
    if show_eval:
        draw_eval(screen, evaluation)
    else:
        # hide old eval bar
        pg.draw.rect(screen, pg.Color(BG_COLOR_ACCENT), pg.Rect(BOARD_WIDTH, 0, EVAL_WIDTH, EVAL_HEIGHT))


def draw_board(screen, board: chess.Board, selected_square):
    """
    Draws all aspects of the board. Includes pieces, squares, and highlights
    :param screen: a pygame canvas
    :param board: a chess board:
    :param selected_square: a tuple of the indices of the last user-selected square, used for highlighting
    """
    draw_squares(screen)
    highlight_check(screen, board)
    highlight_move(screen, selected_square, board)
    draw_pieces(screen, board)


def try_move(selected_squares, board: chess.Board) -> bool:
    """
    Attempt to push a move onto board from the first tuple in
    selected_squares to the second tuple in selected squares.
    :param selected_squares: a pair of (x,y) tuples specifying two squares on board
    :param board: a chess board
    :return: True if move exists in board.legal_moves, false otherwise
    """
    # parse selected squares
    from_square = chess.square(*selected_squares[0])
    to_square = chess.square(*selected_squares[1])

    piece_to_move = board.piece_at(from_square)

    # check if move is a promotion
    promo_choice = None
    if piece_to_move.piece_type == chess.PAWN:
        # TODO: Handle different promotion choices
        if piece_to_move.color == chess.WHITE and chess.square_rank(to_square) == 7:
            promo_choice = chess.QUEEN
        if piece_to_move.color == chess.BLACK and chess.square_rank(to_square) == 0:
            promo_choice = chess.QUEEN

    move = chess.Move(from_square, to_square, promo_choice)

    if move in board.legal_moves:
        board.push(move)
        return True

    return False


def highlight_move(screen, selected_square, board: chess.Board):
    """
    Highlight valid moves from selected_square on screen given board
    :param screen: a pygame canvas
    :param selected_square: a tuple of indices specifying a square on a chess board
    :param board: a chess board
    """

    if selected_square == ():
        # no square is selected
        return

    row, col = selected_square
    square = chess.square(row, col)

    if board.color_at(square) != board.turn:
        # prevents user from clicking opposite colored pieces
        return

    # create highlight surface
    s = pg.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(100)

    # highlight selected_square
    s.fill(pg.Color("purple"))
    screen.blit(s, (row * SQ_SIZE, col * SQ_SIZE))

    # highlight possible moves from selected square
    s.fill(pg.Color("yellow"))
    promotion_highlighted = False
    for move in board.legal_moves:
        if move.from_square == square:
            if move.promotion is not None and promotion_highlighted:
                # prevent promotions from being highlighted multiple times
                continue

            screen.blit(s, (chess.square_file(move.to_square) * SQ_SIZE,
                            chess.square_rank(move.to_square) * SQ_SIZE))

            if move.promotion is not None:
                promotion_highlighted = True


def on_board(location):
    """
    Tests if a location (x, y) is on the chess board.
    :param location: a tuple (x, y) of a location on the screen
    :return: True if both dimensions are within game board, false otherwise
    """
    return all(0 <= dim <= BOARD_WIDTH for dim in location)


def handle_menu_click(clickables, board: chess.Board) -> chess.Board:
    """
    Handles a user click on a menu button
    :param clickables: a list of clickable menu components
    :param board: a chess board:
    :return: an updated chess board, only meaningful in the case of a reset
    """
    for item in clickables:
        if item.is_over(pg.mouse.get_pos()):
            # user is over a clickable button
            if item.id == "reset":
                # reset the board
                board = chess.Board().mirror()
            elif item.id == "eval":
                # TODO: toggle evaluation bar
                item.text = "Hide Evaluation" if item.text == "Show Evaluation" else "Show Evaluation"

    return board


def main():
    """
    Main method of the GUI, used to initialize the window and run central game loop.
    """
    # Initialize window
    pg.init()
    screen = pg.display.set_mode((BOARD_WIDTH + EVAL_WIDTH, BOARD_HEIGHT + MENU_HEIGHT))
    pg.display.set_caption("Chess")
    icon = pg.image.load("assets/window_icon.ico")
    pg.display.set_icon(icon)

    clock = pg.time.Clock()
    screen.fill(pg.Color(BG_COLOR))
    board = chess.Board().mirror()
    load_images()

    # menu components init
    menu_components = []

    width, height = screen.get_width() // 2, MENU_HEIGHT // 2

    # Generate data button
    gen_data_button = Button("data", 0, BOARD_HEIGHT, width, height, "Generate Data")
    menu_components.append(gen_data_button)

    # Train engine button
    train_button = Button("train", width, BOARD_HEIGHT, width, height, "Train")
    menu_components.append(train_button)

    # Reset board button
    reset_button = Button("reset", 0, BOARD_HEIGHT + height, width, height, "Reset Board")
    menu_components.append(reset_button)

    # Show / hide evaluation bar button
    eval_button = Button("eval", width, BOARD_HEIGHT + height, width, height, "Show Evaluation")
    menu_components.append(eval_button)

    show_eval = False
    selected_square = ()
    player_clicks = []

    # Core pygame loop
    running = True
    while running:
        if board.is_game_over():
            # game is over, reset board
            board = chess.Board().mirror()
        for e in pg.event.get():
            if e.type == pg.QUIT:
                # 'X' button has been pressed, stop game
                running = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_r:
                    # 'r' key has been pressed, reset board
                    board = chess.Board().mirror()
            elif e.type == pg.MOUSEBUTTONDOWN:
                # user has clicked
                location = pg.mouse.get_pos()

                if not on_board(location):
                    # Not on chess board, handle menu click
                    board = handle_menu_click(menu_components, board)
                    continue

                # find square indices
                row = int(location[0] // SQ_SIZE)
                col = int(location[1] // SQ_SIZE)

                if selected_square == (row, col):
                    # clicked on same square twice, deselect
                    selected_square = ()
                    player_clicks = []
                    continue

                selected_square = (row, col)
                if board.color_at(chess.square(*selected_square)) != board.turn and len(player_clicks) == 0:
                    # prevent from clicking on empty or opponent pieces
                    continue
                if board.color_at(chess.square(*selected_square)) == board.turn and len(player_clicks) == 1:
                    # reset selections if clicked invalid move
                    player_clicks = []
                player_clicks.append(selected_square)

                if len(player_clicks) == 2:
                    # Player has selected two square, try to make a move
                    if not try_move(player_clicks, board):
                        # Bad move, player!
                        print("Invalid move!")
                    player_clicks = []

        # TODO: implement evaluation
        # TODO: implement engine turn using minimax / neural net

        draw_screen(screen, board, menu_components, selected_square, show_eval=show_eval)
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    # Catch calls and redirect to main method
    main()
