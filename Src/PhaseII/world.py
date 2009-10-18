import pygame
 
class World(object):
    def __init__(self):
        
        self.image = pygame.image.load("bck.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        # [[x1, x2, y], [[x1, x2, y], etc]
        self.solids =[[0,700,450]]