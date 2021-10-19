import pygame
from pygame.surface import Surface
from pygame.rect import Rect
from enum import Enum
import pygame.font
"""
Utils is a file made to contain utility functions used in multiple files,
For the purpose of saving me from cluttering up or having to rewrite the functions
"""

# This file only holds this enum which is used to describe what state the game is in.
class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2
    CUTSCENE = 3
    NEXT_LINE = 4
    RETURN = 5
    MAP = 6

def clamp(value, min, max):
    """
    clamp constrains a value between a min and a max
    """
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

class Button():
    def __init__(self, x: float, y: float, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def render(self, screen: Surface):
        screen.blit(self.image, self.rect)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None) -> Surface:
    """
    Creates a font and renders text, returns the surface blitted to
    TODO: Change the font from sysfont to font.ttf
    """
    font = pygame.font.Font("font.ttf", int(font_size), bold=True)
    surface = font.render(text, False, text_rgb, bg_rgb)
    return surface.convert_alpha()


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
