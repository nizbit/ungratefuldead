import sys, pygame
from pygame.locals import *

class menu():
    def __init__(self, name1, name2):
        self.screen = pygame.display.set_mode((640,480))
        self.bck = pygame.image.load(name1).convert()
        self.marker = pygame.image.load(name2).convert()
        self.rect = self.bck.get_rect()
        self.font = pygame.font.Font("Images/murder.ttf", 30)
        self.colorkey = [0,0,0]
        self.marker.set_colorkey(self.colorkey)
        self.xcord = 0
        self.ycord = 135

        
    def displayText(self):
            self.screen.blit(self.bck, (0,0))
            self.title = self.font.render("Ungreatful Dead", 1, (123,30,30))
            self.start = self.font.render("Start game", 1, (123,30,30))
            self.level1 = self.font.render("Level 1", 1, (123,30,30))
            self.level2 = self.font.render("Level 2", 1, (123,30,30))
            self.quit = self.font.render("Quit", 1, (123,30,30))
            textpos = self.title.get_rect()
            textpos.centerx = self.rect.centerx
            self.screen.blit(self.title, textpos)
            self.screen.blit(self.start, (25,130))
            self.screen.blit(self.quit, (25,290))
            self.screen.blit(self.marker, (self.xcord, self.ycord))
            pygame.display.flip()
            
    def handle_event(self):
        self.running = True
        while self.running:
            print self.ycord
            """loop through the events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if self.ycord >= 290:
                            self.ycord = 130
                        else:
                            self.ycord += 30

                    elif event.key == pygame.K_UP:
                        if self.ycord <= 130:
                            self.ycord = 290
                        else:
                            self.ycord -= 30
                
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit(0)
            
            self.displayText()
                    
        