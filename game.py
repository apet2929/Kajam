import pygame
from pygame.sprite import Sprite
import pygame.draw
import pygame.surface
from utils import *

# This file is where the main game is going to be stored


def mainGame(FPS, clock, screen, images):
    running = True

    while running:
        
        screen.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            
        screen.blit(images[0], (0,0))

        pygame.display.flip()
        clock.tick(FPS)


    return GameState.QUIT


if __name__ == "__main__":
    import gameStateManager
    gameStateManager.main()