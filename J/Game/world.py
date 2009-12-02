import pygame
 
class World(object):
    def __init__(self, image, solids, platform, enemyBounds):
        
        self.image = pygame.image.load(image)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.solids = solids
        self.platform = platform
        self.enemyBounds = enemyBounds