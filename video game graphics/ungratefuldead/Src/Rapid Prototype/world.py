import pygame
 
class World(object):
    def __init__(self):
        
        self.image = pygame.image.load("Images/bck.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.solids =[[0,3800,470]]
        self.platform = [[410,510,398],
                         [540,640,382],
                         [934,1034,408],
                         [1450,1550,405],
                         [1573,1673,377],
                         [1705,1805,371],
                         [2605,2705,407],
                         [2605,2705,362],
                         [2605,2705,319],
                         [2605,2705,274],
                         [2605,2705,223],
                         [2605,2705,168],
                         #[2700,3170,100],
                         [3171,3260,192],
                         [3290,3390,245],
                         [3295,3395,342],
                         [3420,3520,296],
                         [3550,3650,343]]