import pygame
 
class World(object):
    def __init__(self):
        
        self.image = pygame.image.load("Images/bck.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.solids = [pygame.Rect(0, 0, 3800, 10),
                       pygame.Rect(0, 470, 3800, 10),
                       pygame.Rect(0, 0, 10, 470),
                       pygame.Rect(3790, 0, 10, 470)]
        
        self.platform = [pygame.Rect(410, 398,100, 20),
                         pygame.Rect(540, 382,100, 20),
                         pygame.Rect(934, 408,100, 20),
                         pygame.Rect(1450, 405,100, 20),
                         pygame.Rect(1573, 377,100, 20),
                         pygame.Rect(1705, 371,100, 20),
                         pygame.Rect(2605, 407, 100, 20),
                         pygame.Rect(2605,362, 100, 20),
                         pygame.Rect(2605,319, 100, 20),
                         pygame.Rect(2605,274, 100, 20),
                         pygame.Rect(2605,223, 100, 20),
                         pygame.Rect(2605,168, 100, 20),
                         #[2700,3170,100],
                         pygame.Rect(3161,192, 100, 20),
                         pygame.Rect(3290,245, 100, 20),
                         pygame.Rect(3295,372, 100, 20),
                         pygame.Rect(3420,296, 100, 20),
                         pygame.Rect(3550,343, 100, 20)]