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

def loop(buttons: list[UIElement], text:str=None, font:Font=None, pos=None, img:Surface=None):
    # Handles game loop until an action is return by a button in the buttons sprite renderer.
    pass

def titleScreen(title_screen_img):
    start_btn = UIElement(
        center_position=(500, 800),
        font_size=30,
        bg_rgb=(0, 0, 255, 255),
        text_rgb=(255, 0, 255),
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

    running = True
    while running:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill((0, 0, 255))
        
        screen.blit(title_screen_img, (0, 0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
    
        pygame.display.flip()
        clock.tick(FPS)


def loadAssets():
    images = [
        pygame.image.load(join("assets", "temp.png")),
        pygame.image.load(join("assets", "mochi.png"))
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
FPS = 60
clock = pygame.time.Clock()

pygame.init()
screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
main()
pygame.quit()