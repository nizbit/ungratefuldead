import sys, pygame
from pygame.locals import *

class Menu(object):
    def __init__(self, name1, name2):
        self.screen = pygame.display.set_mode((640,480))
        self.bck = pygame.image.load(name1).convert()
        self.marker = pygame.image.load(name2).convert()
        self.rect = self.bck.get_rect()
        self.music = pygame.mixer.Sound("Sounds/zombie_nation.ogg")
        self.music.set_volume(.35)
        self.colorkey = [0,0,0]
        self.marker.set_colorkey(self.colorkey)
        self.xcord = 50
        self.ycord = 200
        
    def update(self):
        self.screen.blit(self.bck, (0,0))
        self.screen.blit(self.marker, (self.xcord, self.ycord))
        pygame.display.flip()
        
    def handle_event(self):
        self.music.play()
        self.running = True
        while self.running:
            """loop through the events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #self.running = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_DOWN:
                        self.ycord += 25
                    elif event.key == pygame.K_UP:
                        self.ycord -= 25
                    elif event.key == pygame.K_RETURN:
                        if self.ycord == 200:
                            self.music.stop()
                            return 1
                        elif self.ycord == 225:
                            self.music.stop()
                            return 2
                        elif self.ycord == 275:
                            self.music.stop()
                            return 0
                
            if self.ycord >= 280:
                self.xcord = 50
                self.ycord = 200
            if self.ycord > 225 and self.xcord == 50:
                self.xcord = 25
                self.ycord = 275
            if self.ycord < 275 and self.ycord > 195 and self.xcord == 25:
                self.xcord = 50
                self.ycord = 225
            if self.ycord <= 195:
                self.xcord = 25
                self.ycord = 275
            self.update()
                    
        