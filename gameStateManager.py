import pygame
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
import game
from utils import *


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
    
    # Images will get passed to gamme.py
    # Supplying its assets to it 
    # For simplicity sake they will be loaded on compilation

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
            nextState = game.mainGame(FPS, clock, screen, images)
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