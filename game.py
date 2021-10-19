import pygame
from pygame.constants import SHOWN
from pygame.math import Vector2
from pygame.sprite import Group, Sprite
import pygame.draw
import pygame.surface
from utils import *
from pygame.image import load
from os.path import join
import pygame.mouse
import pygame.transform
import pygame.sprite
import pygame.time
import pygame.event

# This file is where the main game is going to be stored

# TODO: Add more enemy types
class EnemyType(Enum):
    BASIC = 0

class Tower(Sprite):
    towers = Group()
    def __init__(self, image: Surface, position: tuple) -> None:
        super().__init__()
        self.image = pygame.transform.scale(image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        # Radius of the targetting range circle
        self.rangeRadius: int = 1000
        
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
        if len(Enemy.enemies.sprites()) == 0:
            return False

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

        if closestDistance > self.rangeRadius:
            # Enemy isn't within tower's range
            return False

        # Shoots bullet
        Bullet.genBullet(0, Vector2(self.rect.centerx, self.rect.centery), target=Vector2(closest.rect.x, closest.rect.y))
        return True


class Bullet(Sprite):

    SPEED = 200
    bullets = Group()
    images = []
    def __init__(self, type: int, position: Vector2, velocity: Vector2) -> None:
        super().__init__()
        self.type = type
        try:
            self.image = Bullet.images[type]
        except IndexError:
            print("Bullet type" + str(type) + " does not exist!")
            return
        
        self.image = pygame.transform.scale(self.image, (25,25))
        self.rect = self.image.get_rect()
        self.pos = position
        self.rect.centerx = position.x
        self.rect.centery = position.y
        self.velocity = velocity
        if self.type == 0:
            self.damage = 5
        elif self.type == 1:
            self.damage = 15
        elif self.type == 2:
            self.damage = 51

    def update(self, delta):
        self.pos += self.velocity * delta
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        # Clamping position within bounds of screen
        if (self.rect.top > SCREEN_HEIGHT) or (self.rect.left > SCREEN_WIDTH) or (self.rect.bottom < 0) or (self.rect.right < 0):
            self.kill()
    
    def genBullet(type: int, sourcePos: Vector2, target: Vector2):

        # Bullet calculations
        bulletVel = target - sourcePos
        bulletVel.scale_to_length(Bullet.SPEED)
    
        bullet = Bullet(type, position=sourcePos, velocity=bulletVel)
        Bullet.bullets.add(bullet)

        # Returns bullet just in case we need it, in most cases we don't
        return bullet

class EnemySpawner():
    """
    send_next_event tells the game to send the next enemy
    round_over_event tells the game that the round is over
    """
    next_enemy_event = pygame.USEREVENT + 1
    round_over_event = pygame.USEREVENT + 2

    def __init__(self, enemyList, delayList):
        """
        self.enemies is a list of Enemy, each enemy in the list has a corresponding value in the delayList
        the value in the delayList represents the amount of time to be waited before spawning the next enemy

        IMPORTANT: enemyList must be the same length as delayList
        """
    
        self.enemyList: list[Enemy] = enemyList
        self.delayList: list[float] = delayList
    def start(self):
        """pygame.USEREVENT + 1 is going to say 'Spawn the next enemy' basically"""
        pygame.time.set_timer(EnemySpawner.next_enemy_event, self.delayList[0])
        print("Starting round")
    
    def spawnNextEnemy(self):
        """
        Removes the first enemy from EnemySpawner list and adds it to the enemies group,
        Creates a timer to spawn the next one
        """
        print("Spawning next enemy")
        Enemy.enemies.add(self.enemyList.pop(0))

        # No more enemies left
        if len(self.enemyList) == 0:
            pygame.event.post(pygame.event.Event(EnemySpawner.round_over_event))
        else:
            # The 1 in set_timer tells the program not to loop
            pygame.time.set_timer(EnemySpawner.next_enemy_event, self.delayList.pop(0), 1)


# TODO: Have enemies follow bezier curve
class Enemy(Sprite):
    enemies = Group()
    path = list[Vector2] #  The path the enemies will follow
    def __init__(self, image, type): 
        super().__init__()
        self.type = type
        # TODO: have list of images, 1 per enemy type, and have enemy type decide the image
        self.image = image
        
        self.rect = image.get_rect()
        self.rect.x = Enemy.path[0].x
        self.rect.y = Enemy.path[1].y

        """
        time_alive is used to track how long the enemy has been alive and directly corresponds to its position on the map
        """
        self.time_alive = 0
        
        """
        type corresponds to the EnemyType Enum
        It determines the sprite, speed, health, and any other attributes that I decide
        """
        if self.type == EnemyType.BASIC:
            self.health = 100
            self.max_time = 10
        else:
            self.health = 10
            self.max_time = 20

    def update(self, delta):
        """
        Enemy position is updated based on delta
        Enemy position is CONSISTENT- give 2 enemies the same time alive, and they will have the same position
        Delta represents the change in time between frames in seconds- usually a number less than 0
        """

        self.time_alive += delta
        if self.time_alive > self.max_time:
            # Deal damage to player
            print("Hit end of path")
            self.kill()

        pos = (1-self.time_alive/self.max_time)**3 * Enemy.path[0] + 3*(1-self.time_alive/self.max_time)**2 * self.time_alive/self.max_time * Enemy.path[1] + 3 * (1-self.time_alive/self.max_time) * (self.time_alive/self.max_time)**2 * Enemy.path[2] + (self.time_alive/self.max_time)**3 * Enemy.path[3]
        self.rect.x = pos.x
        self.rect.y = pos.y


    def onCollision(self, bullet: Bullet):
        self.health -= bullet.damage
        if self.health < 0:
            self.kill()
            print("Oof I ded")
        bullet.kill()


def mainGame(FPS, clock, screen, images):
    running = True
    
    mapPath = [
        Vector2(0,0),
        Vector2(SCREEN_WIDTH*0.8, SCREEN_HEIGHT*0.2),
        Vector2(SCREEN_WIDTH*0.2, SCREEN_HEIGHT * 0.8),
        Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)
    ]
    Enemy.path = mapPath

    # Add test enemy
    Enemy.enemies.add()
    Bullet.images.extend([
        images["bullet1.jpg"],
        images["bullet2.png"],
        images["bullet3.jpg"]
    ])

    # Add test tower
    Tower.towers.add(Tower(images["mochi.png"], (500,300)))

    spawner = EnemySpawner(
        enemyList=[
            Enemy(images["mochi.png"], EnemyType.BASIC),
            Enemy(images["mochi.png"], EnemyType.BASIC),
            Enemy(images["mochi.png"], EnemyType.BASIC)
        ],
        delayList=[
            500, 2000, 50
        ]
    )
    pygame.time.set_timer(pygame.USEREVENT + 3, 500, 1)

    while running:
        delta = clock.tick(FPS) / 1000
        screen.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            elif event.type == pygame.MOUSEBUTTONUP:
                # Temporary, start the round on mousebuttonup
                spawner.start()
            elif event.type == EnemySpawner.next_enemy_event:
                spawner.spawnNextEnemy()
            elif event.type == EnemySpawner.round_over_event:
                # Round over, do stuff here
                print("No more enemies")
                pass
                
            elif event.type == pygame.USEREVENT + 3:
                print("yee test")

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