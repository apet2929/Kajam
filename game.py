import pygame
from pygame.math import Vector2
from pygame.sprite import Group, Sprite
import pygame.draw
import pygame.surface
from utils import *
from pygame.image import load
from os.path import join

# This file is where the main game is going to be stored

# TODO: Have enemies follow bezier curve
class Enemy(Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = Rect(0,0,50,50)

        # I have to use a separate positon vector2 because rect tracks using ints which won't be good enough for the level 
        # Of precision we need
        self.pos = Vector2(0,0)
        self.time_alive = 0

    def update(self, delta):
        """
        Enemy position is updated based on delta
        Enemy position is CONSISTENT- give 2 enemies the same time alive, and they will have the same position
        Delta represents the change in time between frames in seconds- usually a number less than 0
        """
        self.time_alive += delta
        
        self.pos += Vector2(50 * delta, 50 * delta)

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

def mainGame(FPS, clock, screen, images):
    running = True

    enemyImage = load(join("assets", "mochi.png"))
    enemies = Group()
    enemies.add(Enemy(enemyImage))


    while running:
        delta = clock.tick(FPS) / 1000
        screen.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            
        # screen.blit(images[0], (0,0))

        enemies.update(delta)

        enemies.draw(screen)

        pygame.display.flip()
        


    return GameState.QUIT


if __name__ == "__main__":
    import gameStateManager
    gameStateManager.main()