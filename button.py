import pygame
from pygame.surface import Surface
class Button():
    def __init__(self, x: float, y: float, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def render(self, screen: Surface):
        screen.blit(self.image, self.rect)
