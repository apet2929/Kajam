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
import pygame.time

# This file is where the main game is going to be stored

class Tower(Sprite):
    towers = Group()
    def __init__(self, image: Surface, position: tuple) -> None:
        super().__init__()
        self.image = pygame.transform.scale(image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        # Radius of the targetting range circle
        self.rangeRadius: int = 100
        
        # Attack cooldown - time between shooting bullets in seconds
        # Doesn't change, this is constant
        self.cooldown: int = 2
        self.cooldownCounter = 0
        self.inCooldown: bool = False

    def update(self, delta):
        if self.inCooldown:
            self.cooldownCounter += delta
            if self.cooldownCounter > self.cooldown:
                # Cooldown ended
                self.cooldownCounter = 0
                self.inCooldown = False
                
        else:
            # Shoot bullet
            if self.shootBullet():
                self.inCooldown = True

    def shootBullet(self):
        selfPos = Vector2(self.rect.x, self.rect.y)

        # Get closest enemy
        closest = None
        closestDistance = None

        enemy: Enemy
        for enemy in Enemy.enemies.sprites():
            
            enemyPos = Vector2(enemy.rect.centerx, enemy.rect.centery)
            if closest:  
                if enemyPos.distance_to(selfPos) < closestDistance:
                    closest = enemy
                    closestDistance = enemyPos.distance_to(selfPos)
            else:
                closest = enemy
                closestDistance = enemyPos.distance_to(selfPos)

        if not closest:
            return False
        Bullet.genBullet(0, Vector2(self.rect.x, self.rect.y), target=Vector2(closest.rect.x, closest.rect.y))
        return True


class Bullet(Sprite):

    SPEED = 200
    bullets = Group()
    images = []
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
    
    def genBullet(image: Surface or int, sourcePos: Vector2, target: Vector2):
        mousePos = pygame.mouse.get_pos()

        # Bullet calculations
        bulletVel = target - sourcePos
        bulletVel.scale_to_length(Bullet.SPEED)
        
        if type(image) == int:
            im = Bullet.images[image]
        else:
            im = image
        bullet = Bullet(im, position=sourcePos, velocity=bulletVel)
        Bullet.bullets.add(bullet)

        # Returns bullet just in case we need it, in most cases we don't
        return bullet


# TODO: Have enemies follow bezier curve
class Enemy(Sprite):
    enemies = Group()
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = Rect(200,0,50,50)

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




def mainGame(FPS, clock, screen, images):
    running = True
    
    Enemy.enemies.add(Enemy(images[1]))
    Bullet.images.append(images[0]) 
    Tower.towers.add(Tower(images[1], (500,300)))

    while running:
        delta = clock.tick(FPS) / 1000
        screen.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == pygame.MOUSEBUTTONUP:
                # Creates a bullet and adds it to the bullet group
                mouseX, mouseY = pygame.mouse.get_pos()
                Bullet.genBullet(images[0], Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), Vector2(mouseX, mouseY))
            
        # screen.blit(images[0], (0,0))
        Tower.towers.update(delta)
        Enemy.enemies.update(delta)
        Bullet.bullets.update(delta)

        # Enemy collision with bullets

        collisions = pygame.sprite.groupcollide(Enemy.enemies, Bullet.bullets, False, True)
        enemy: Enemy
        for enemy in Enemy.enemies:
            try:
                for bullet in collisions[enemy]:
                    enemy.onCollision(bullet)
            except KeyError:
                # Enemy is not colliding with anything
                pass

        Bullet.bullets.draw(screen)
        Enemy.enemies.draw(screen)
        Tower.towers.draw(screen)

        pygame.display.flip()
    

    return GameState.QUIT


if __name__ == "__main__":
    import gameStateManager
    gameStateManager.main()