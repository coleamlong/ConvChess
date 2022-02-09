import pygame as pg
from button import Button
import chess

BUTTON_COLOR = (230, 230, 230)
HIGHLIGHT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (200, 200, 200)
OUTLINE_PADDING = .05
TEXT_SCALE = 0.7
TEXT_COLOR = (32, 32, 32)

CHOICES = ["knight", "bishop", "rook", "queen"]


class PromotionSelector:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.choice = None
        self.buttons = []

        button_height = self.height // (len(CHOICES) + 1)

        index = 0
        for choice in CHOICES:
            choice_button = Button(choice, self.x, self.y + button_height * index,
                                   self.width, button_height, choice.capitalize())
            self.buttons.append(choice_button)
            index += 1

        submit_button = Button("submit", self.x, self.y + button_height * index, self.width, button_height, "Submit")
        self.buttons.append(submit_button)

    def draw(self, screen):
        for button in self.buttons:
            print("drawing button:", button.id)
            button.draw(screen)

    def get_selection(self) -> chess.PieceType:
        print("test")
        promo_choices = {
            "knight": chess.KNIGHT,
            "bishop": chess.BISHOP,
            "rook": chess.ROOK,
            "queen": chess.QUEEN,
        }
        choice = None
        submitted = False
        while not submitted:
            for e in pg.event.get():
                for button in self.buttons:
                    if button.is_over(pg.mouse.get_pos()) and e.type == pg.MOUSEBUTTONDOWN:
                        if button.id == "submit":
                            if choice is not None:
                                submitted = True
                        else:
                            choice = promo_choices[button.id]

        return choice
