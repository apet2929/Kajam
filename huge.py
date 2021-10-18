import pygame
from enum import Enum
import pygame.rect
from pygame.rect import Rect
import pygame.event
import pygame.draw
from pygame.surface import Surface
import pygame.freetype
from pygame.font import *
from pygame.sprite import RenderUpdates
import pygame.image
from os.path import join

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2
    CUTSCENE = 3
    NEXT_LINE = 4
    RETURN = 5
    MAP = 6


class UIElement(pygame.sprite.Sprite):

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        super().__init__()

        self.mouse_over = False

        default_image = create_surface_with_text(
            text, font_size, text_rgb, bg_rgb)

        highlighted_image = create_surface_with_text(
            text, font_size * 1.2, text_rgb, bg_rgb)

        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position)]

        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False


def clamp(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None) -> Surface:
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

def loop(buttons: list[UIElement], text:str=None, font:Font=None, pos=None, img:Surface=None):
    # Handles game loop until an action is return by a button in the buttons sprite renderer.
    running = True
    while running:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill((0, 0, 255))
        if img is not None:
            screen.blit(img, (0, 0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)

        if text is not None and pos is not None:
            drawText(screen, text, (0,0,255), pos, font, True)
    

        pygame.display.flip()
        clock.tick(FPS)


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

def game(images):
    running = True

    while running:
        print("yee")
        
        screen.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            
        screen.blit(images[0], (0,0))

        pygame.display.flip()
        clock.tick(FPS)

def titleScreen(title_screen_img):
    start_btn = UIElement(
        center_position=(500, 400),
        font_size=30,
        bg_rgb=(0, 0, 255, 255),
        text_rgb=(255, 255, 255),
        text="Start",
        action=GameState.NEWGAME
    )

    quit_btn = UIElement(
        center_position=(500, 500),
        font_size=30,
        bg_rgb=(0, 0, 255),
        text_rgb=(255, 255, 255),
        text="Quit",
        action=GameState.QUIT
    )

    title_text = UIElement(
        center_position=(500, 250),
        font_size=60,
        bg_rgb=(0, 0, 255),
        text_rgb=(255, 255, 255),
        text="Kajam Game",
        action=None
    )

    buttons = RenderUpdates(start_btn, quit_btn, title_text)

    return loop(buttons, img=title_screen_img)

def loadAssets():
    images = [
        pygame.image.load(join("assets", "temp.png"))
    ]
    return images

def main():
    game_state = GameState.TITLE
    
    images = loadAssets()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = GameState.QUIT
            

        nextState = None
        if game_state == GameState.QUIT:
            running = False
        elif game_state == GameState.TITLE:
            nextState = titleScreen(images[0])
        elif game_state == GameState.CUTSCENE:
            pass
        elif game_state == GameState.NEWGAME:
            nextState = game(images)
        elif game_state == GameState.NEXT_LEVEL:
            pass
            
        game_state = nextState


#  Constant Variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

FPS = 60
clock = pygame.time.Clock()

pygame.init()
screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
main()
pygame.quit()