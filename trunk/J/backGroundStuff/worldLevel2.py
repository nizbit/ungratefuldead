import pygame
 
class World(object):
    def __init__(self):
        
        self.image = pygame.image.load("level2.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.solids =[[0,3800,365]]
        self.platform = [[334,449,343],
                         [450,565,288],
                         [1520,1745,295],
                         [1870,1985,244],
                         [2140,2255, 241],
                         [2487,2602,287],
                         [2994,3113,240]]
                         
                         
                         
 