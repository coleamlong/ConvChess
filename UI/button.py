import pygame as pg

BUTTON_COLOR = (230, 230, 230)
HIGHLIGHT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (200, 200, 200)
OUTLINE_PADDING = .05
TEXT_SCALE = 0.7
TEXT_COLOR = (32, 32, 32)


class Button:
    def __init__(self, id: str, x, y, width, height, text=""):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def set_text(self, text: str):
        self.text = text

    def draw(self, screen, outline=False):
        # Call this method to draw the button on the screen
        if outline:
            outline_x = self.x - (self.width * OUTLINE_PADDING)
            outline_y = self.y - (self.height * OUTLINE_PADDING)
            outline_width = self.width + (2 * self.width * OUTLINE_PADDING)
            outline_height = self.height + (3 * self.height * OUTLINE_PADDING)
            pg.draw.rect(screen, pg.Color(OUTLINE_COLOR),
                         pg.Rect(outline_x, outline_y, outline_width, outline_height))

        color = BUTTON_COLOR
        if self.is_over(pg.mouse.get_pos()):
            color = HIGHLIGHT_COLOR
        pg.draw.rect(screen, color, pg.Rect(self.x, self.y, self.width, self.height))

        if self.text != "":
            font = pg.font.SysFont(None, int(min(self.width, self.height) * TEXT_SCALE))
            text = font.render(self.text, True, pg.Color(TEXT_COLOR))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, location):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < location[0] < self.x + self.width:
            if self.y < location[1] < self.y + self.height:
                return True

        return False
