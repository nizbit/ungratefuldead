import sys, pygame
from pygame.locals import *

class Menu(object):
    def __init__(self, name1, name2):
        self.screen = pygame.display.set_mode((640,480))
        self.bck = pygame.image.load(name1).convert()
        self.marker = pygame.image.load(name2).convert()
        self.rect = self.bck.get_rect()
        self.font = pygame.font.Font("Images/murder.ttf", 30)
        self.colorkey = [0,0,0]
        self.marker.set_colorkey(self.colorkey)
        self.xcord = 50
        self.ycord = 150
        
    def update(self):
        self.screen.blit(self.bck, (0,0))
        self.screen.blit(self.marker, (self.xcord, self.ycord))
        pygame.display.flip()
        
    def handle_event(self):
        self.running = True
        while self.running:
            """loop through the events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_DOWN:
                        self.ycord += 25
                    elif event.key == pygame.K_UP:
                        self.ycord -= 25
                    elif event.key == pygame.K_RETURN:
                        if self.ycord == 200:
                            return 1
                        elif self.ycord == 225:
                            return 2
                        elif self.ycord == 275:
                            return 0
                print self.xcord
                print self.ycord
            if self.ycord >= 280:
                self.xcord = 50
                self.ycord = 200
            if self.ycord <= 195:
                self.xcord = 25
                self.ycord = 275
            if self.ycord > 225 and self.xcord == 50:
                self.xcord = 25
                self.ycord = 275
            if self.ycord < 275 and self.xcord == 25:
                self.xcord = 50
                self.ycord = 225
            
            self.update()
                    
        