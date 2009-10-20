import pygame
from pygame.locals import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, name, x_offset, y_offset):
        self.image = pygame.image.load(name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left += x_offset
        self.rect.top += y_offset
        
        self.image.set_colorkey((0,0,0), RLEACCEL)
        