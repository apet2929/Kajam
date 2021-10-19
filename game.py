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
import pygame.sprite

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
        self.damage = 51

    def update(self, delta):
        self.pos += self.velocity * delta
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        # Clamping position within bounds of screen
        if (self.rect.top > SCREEN_HEIGHT) or (self.rect.left > SCREEN_WIDTH) or (self.rect.bottom < 0) or (self.rect.right < 0):
            self.kill()
    
    def genBullet(bullets: Group, image: Surface, sourcePos: Vector2):
        mousePos = pygame.mouse.get_pos()

        # Bullet calculations
        bulletVel = Vector2(mousePos[0], mousePos[1]) - sourcePos
        bulletVel.scale_to_length(Bullet.SPEED)
        
        bullet = Bullet(image, position=sourcePos, velocity=bulletVel)
        bullets.add(bullet)
        return bullet


# TODO: Have enemies follow bezier curve
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, point1, point2, point3, point4, time): #points are tuples
        #andrew pls help i still dont know how to do time
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.p1 = Vector2(point1[0], point1[1])
        self.p2 = Vector2(point2[0], point2[1])
        self.p3 = Vector2(point3[0], point3[1])
        self.p4 = Vector2(point4[0], point4[1])
        self.t = 0
        self.goingUp = True

        self.pos = Vector2(point1[0], point1[1])
        self.time_alive = 0
        self.health = 100
        self.damage = 101

    def update(self): #, delta
        """
        Enemy position is updated based on delta
        Enemy position is CONSISTENT- give 2 enemies the same time alive, and they will have the same position
        Delta represents the change in time between frames in seconds- usually a number less than 0
        """
        self.pos = (1-self.t/100)**3 * self.p1 + 3*(1-self.t/100)**2 * self.t/100 * self.p2 + 3 * (1-self.t/100) * (self.t/100)**2 * self.p3 + (self.t/100)**3 * self.p4

        # self.time_alive += delta
        # self.pos += Vector2(50 * delta, 50 * delta)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.goingUp:
            self.t += 1
        
        if self.goingUp == False:
            self.t -= 1
        
        if self.t >= 100:
            self.goingUp = False
        if self.t <= 0:
            self.goingUp = True


    # def onCollision(self, bullet: Bullet):
    #     self.health -= bullet.damage
    #     if self.health < 0:
    #         self.kill()
    #         print("Oof I ded")
    #     bullet.kill()
    def render(self):
        screen.blit(self.image, (self.pos.x, self.pos.y))




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
                # Creates a bullet and adds it to the bullet group
                Bullet.genBullet(bullets, images[0], Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            
        # screen.blit(images[0], (0,0))

        enemies.update(delta)
        bullets.update(delta)

        # Enemy collision with bullets

        collisions = pygame.sprite.groupcollide(enemies, bullets, False, True)
        enemy: Enemy
        for enemy in enemies:
            try:
                for bullet in collisions[enemy]:
                    enemy.onCollision(bullet)
            except KeyError:
                # Enemy is not colliding with anything
                pass

        bullets.draw(screen)
        enemies.draw(screen)

        pygame.display.flip()

    return GameState.QUIT


if __name__ == "__main__":
    import gameStateManager
    gameStateManager.main()