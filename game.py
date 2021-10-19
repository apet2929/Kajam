import pygame
from pygame.math import Vector2
from pygame.sprite import Group, Sprite
import pygame.draw
import pygame.surface
from utils import *
from pygame.image import load
from os.path import join
import pygame.mouse
import gameStateManager
import pygame.transform

# This file is where the main game is going to be stored


class Bullet(Sprite):

    SPEED = 200
    # TODO: Have bullets rotate and point to the correct position
    def __init__(self, image: Surface, position: Vector2, velocity: Vector2) -> None:
        super().__init__()
        self.image = pygame.transform.scale(image, (50,50))
        self.rect = self.image.get_rect()
        self.pos = position
        self.rect.x = position.x
        self.rect.y = position.y
        self.velocity = velocity


    def update(self, delta):
        self.pos += self.velocity * delta
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        # Clamping position within bounds of screen
        if (self.rect.top > SCREEN_HEIGHT) or (self.rect.left > SCREEN_WIDTH) or (self.rect.bottom < 0) or (self.rect.right < 0):
            self.kill()

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
        self.health = 100
        self.damage = 101

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

    def onCollision(self, bullet: Bullet):
        self.health -= bullet.damage
        if self.health < 0:
            self.kill()
            print("Oof I ded")
        bullet.kill()



def genBullet(bullets: Group, image: Surface, sourcePos: Vector2):
    mousePos = pygame.mouse.get_pos()

    # Bullet calculations
    bulletVel = Vector2(mousePos[0], mousePos[1]) - sourcePos
    bulletVel.scale_to_length(Bullet.SPEED)
    
    bullet = Bullet(image, position=sourcePos, velocity=bulletVel)
    bullets.add(bullet)

def mainGame(FPS, clock, screen, images):
    running = True

    enemyImage = load(join("assets", "mochi.png"))
    enemies = Group()
    bullets = Group()
    enemies.add(Enemy(enemyImage))


    while running:
        delta = clock.tick(FPS) / 1000
        screen.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == pygame.MOUSEBUTTONUP:
                genBullet(bullets, images[0], Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            
        # screen.blit(images[0], (0,0))

        enemies.update(delta)
        bullets.update(delta)

        bullets.draw(screen)
        enemies.draw(screen)

        pygame.display.flip()
        


    return GameState.QUIT


if __name__ == "__main__":
    import gameStateManager
    gameStateManager.main()