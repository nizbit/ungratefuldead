import sys, pygame, menu
from pygame.locals import *

class InGame(menu.Menu):
    def __init__(self, name1, name2):
        super(InGame, self).__init__(name1, name2)
        self.xcord = 5
        self.ycord = 300

        
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
                        self.ycord += 85
                    elif event.key == pygame.K_UP:
                        self.ycord -= 85
                    elif event.key == pygame.K_RETURN:
                        if self.ycord == 300:
                            return 1
                        elif self.ycord == 385:
                            return 0

            if self.ycord > 385:
                self.ycord = 300
            if self.ycord < 300:
                self.ycord = 385
            
            self.update()