import random

import pygame as pg
import chess
import itertools
from button import Button

SCALE = .5
BOARD_WIDTH, BOARD_HEIGHT = 512 * SCALE, 512 * SCALE
EVAL_WIDTH, EVAL_HEIGHT = 32 * SCALE, BOARD_HEIGHT
MENU_WIDTH, MENU_HEIGHT = BOARD_WIDTH + EVAL_WIDTH, 128 * SCALE

BG_COLOR = (63, 63, 63)
BG_COLOR2 = (127, 127, 127)

BOARD_SIZE = 8
SQ_SIZE = BOARD_WIDTH // BOARD_SIZE
MAX_FPS = 30
IMAGES = {}


def load_images():
    for color in chess.COLOR_NAMES:
        for piece in chess.PIECE_NAMES:
            if piece is None:
                continue

            piece_name = f"{color}_{piece}"
            IMAGES[piece_name] = \
                pg.transform.smoothscale(pg.image.load(f"assets/pieces/{piece_name}.png"), (SQ_SIZE, SQ_SIZE))


def draw_squares(screen):
    color = itertools.cycle([pg.Color("white"), pg.Color("gray")])
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            pg.draw.rect(screen, next(color), pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        next(color)


def draw_pieces(screen, board: chess.Board):
    for square in chess.SQUARES:
        chess_piece = board.piece_at(square)
        if chess_piece is None:
            continue

        piece_color = chess.COLOR_NAMES[0] if chess_piece.color else chess.COLOR_NAMES[1]
        piece_name = f"{piece_color}_{chess.piece_name(chess_piece.piece_type)}"
        row = chess.square_rank(square)
        col = chess.square_file(square)
        screen.blit(IMAGES[piece_name], pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_check(screen, board):
    if board.is_check():
        s = pg.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(200)
        s.fill(pg.Color("red"))
        king_square = board.king(board.turn)
        screen.blit(s, (chess.square_file(king_square) * SQ_SIZE, chess.square_rank(king_square) * SQ_SIZE))


def draw_eval(screen, evaluation):
    pg.draw.rect(screen, pg.Color("white"), pg.Rect(BOARD_WIDTH, 0, EVAL_WIDTH, EVAL_HEIGHT))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(BOARD_WIDTH, 0, EVAL_WIDTH, EVAL_HEIGHT * (evaluation / 2000) + (EVAL_HEIGHT / 2)))
    pass


def draw_menu(screen, menu_components, board):
    for item in menu_components:
        item.draw(screen, False)
    pass


def draw_screen(screen, board: chess.Board, menu_components ,selected_square, show_eval=False, evaluation=0):
    draw_menu(screen, menu_components, board)
    draw_board(screen, board, selected_square)
    if show_eval:
        draw_eval(screen, evaluation)
    else:
        pg.draw.rect(screen, pg.Color(BG_COLOR2), pg.Rect(BOARD_WIDTH, 0, EVAL_WIDTH, EVAL_HEIGHT))


def draw_board(screen, board: chess.Board, selected_square):
    draw_squares(screen)
    highlight_check(screen, board)
    highlight_move(screen, selected_square, board)
    draw_pieces(screen, board)


def get_promo_choice(screen) -> chess.PieceType:
    promo_choice = {
        'n': chess.KNIGHT,
        'b': chess.BISHOP,
        'r': chess.ROOK,
        'q': chess.QUEEN,
    }
    user_input = input("Promo Choice (n, b, r, q):").lower()
    return promo_choice.get(user_input)


def try_move(screen, selected_squares, board: chess.Board) -> bool:
    # parse selected squares
    from_square = chess.square(*selected_squares[0])
    to_square = chess.square(*selected_squares[1])

    piece_to_move = board.piece_at(from_square)
    promo_choice = None
    if piece_to_move.piece_type == chess.PAWN:
        if piece_to_move.color == chess.WHITE and chess.square_rank(to_square) == 7:
            promo_choice = get_promo_choice(screen)
        if piece_to_move.color == chess.BLACK and chess.square_rank(to_square) == 0:
            promo_choice = get_promo_choice(screen)

    move = chess.Move(from_square, to_square, promo_choice)

    if move in board.legal_moves:
        board.push(move)
        return True

    return False


def highlight_move(screen, selected_square, board: chess.Board):
    if selected_square == ():
        return

    row, col = selected_square
    square = chess.square(row, col)

    if board.color_at(square) != board.turn:
        return

    s = pg.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(100)

    s.fill(pg.Color("purple"))
    screen.blit(s, (row * SQ_SIZE, col * SQ_SIZE))

    s.fill(pg.Color("yellow"))
    promotion_highlighted = False
    for move in board.legal_moves:
        if move.from_square == square:
            if move.promotion is not None and promotion_highlighted:
                continue

            screen.blit(s, (chess.square_file(move.to_square) * SQ_SIZE, chess.square_rank(move.to_square) * SQ_SIZE))
            if move.promotion is not None:
                promotion_highlighted = True


def on_board(location):
    return all(0 <= dim <= BOARD_WIDTH for dim in location)


def handle_menu_click(menu_components, board: chess.Board) -> chess.Board:
    for item in menu_components:
        if item.is_over(pg.mouse.get_pos()):
            if item.id == "reset":
                board = chess.Board().mirror()
            elif item.id == "eval":
                item.text = "Hide Evaluation" if item.text == "Show Evaluation" else "Show Evaluation"
    return board


def main():
    pg.init()
    screen = pg.display.set_mode((BOARD_WIDTH + EVAL_WIDTH, BOARD_HEIGHT + MENU_HEIGHT))
    pg.display.set_caption("Chess")
    icon = pg.image.load("assets/window_icon.ico")
    pg.display.set_icon(icon)

    clock = pg.time.Clock()
    screen.fill(pg.Color(BG_COLOR))
    board = chess.Board().mirror()
    load_images()

    # promotion selector

    # menu components init
    menu_components = []
    # reset button
    # +/- scale
    width, height = screen.get_width() // 2, MENU_HEIGHT // 2
    gen_data_button = Button("data", 0, BOARD_HEIGHT, width, height, "Generate Data")
    menu_components.append(gen_data_button)
    train_button = Button("train", width, BOARD_HEIGHT, width, height, "Train")
    menu_components.append(train_button)
    reset_button = Button("reset", 0, BOARD_HEIGHT + height, width, height, "Reset Board")
    menu_components.append(reset_button)
    eval_button = Button("eval", width, BOARD_HEIGHT + height, width, height, "Show Evaluation")
    menu_components.append(eval_button)
    # Hide/show eval
    show_eval = False
    # Turn display

    selected_square = ()
    player_clicks = []
    running = True
    while running:
        if board.is_game_over():
            board = chess.Board().mirror()
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_r:
                    board = chess.Board().mirror()
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                if not on_board(location):
                    board = handle_menu_click(menu_components, board)
                    continue
                row = location[0] // SQ_SIZE
                col = location[1] // SQ_SIZE

                if selected_square == (row, col):
                    selected_square = ()
                    player_clicks = []
                    continue

                selected_square = (row, col)
                if board.color_at(chess.square(*selected_square)) != board.turn and len(player_clicks) == 0:
                    continue
                if board.color_at(chess.square(*selected_square)) == board.turn and len(player_clicks) == 1:
                    player_clicks = []
                player_clicks.append(selected_square)

                if len(player_clicks) == 2:
                    if not try_move(screen, player_clicks, board):
                        print("Invalid move!")
                    player_clicks = []

        eval = random.randint(-1000, 1000)
        draw_screen(screen, board, menu_components, selected_square, show_eval=show_eval, evaluation=eval)
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
