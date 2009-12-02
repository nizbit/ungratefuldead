import math
import sys, pygame
from pygame.locals import *


class Status(object):
    def __init__ (self, screen, fontPath):
        
        self.myScreen = screen 
        self.font = pygame.font.Font(fontPath, 30)

        self.hCord_x = 5
        self.hCord_y = 5
        
        self.hBar_x = self.hCord_x - 1
        self.hBar_y = self.hCord_y + 2
        self.hBar_height = 17
    
        self.sCord_x = 5
        self.sCord_y = 45
        
        self.lCord_x = 5
        self.lCord_y = 25
        
        self.outLineRectColor = (255,255,255)
        self.hpBarColor = (0,0,255)
        self.labelColor = (255,255,255)
        
        self.jCounter = 0;
        
    def upDate(self, healthPoints, score, lives):
        
        healthPoints = 30
        
        if self.jCounter >= 7:
            self.jCounter = 0
        else:
            self.jCounter += .25
        
        offSet = math.floor(15 * math.sin(self.jCounter))
        
        lGreen = (32,172,44)
        lAmber = (225,194,91)
        lRed   = (155 + offSet,20 + offSet,20 + offSet)
        
        if healthPoints <= 70:
            self.hpBarColor = lAmber
            if healthPoints <= 40:
                self.hpBarColor = lRed
        else:
            self.hpBarColor = lGreen  
        
        
        self.healthPointTxt = self.font.render("HP:", 1, self.labelColor)
        self.hpNumTxt = self.font.render(str(healthPoints), 1, self.labelColor)
        self.scoreTxt = self.font.render("Score: " + str(score), 1, self.labelColor)
        self.liveTxt  = self.font.render("Lives: " + str(lives), 1, self.labelColor)    
        
        # HP Label
        self.myScreen.blit(self.healthPointTxt, (self.hCord_x, self.hCord_y))
        # HP Num
        self.myScreen.blit(self.hpNumTxt, (self.hCord_x + 140, self.hCord_y))
        # Lives
        self.myScreen.blit(self.liveTxt, (self.lCord_x, self.lCord_y))
        # Score
        self.myScreen.blit(self.scoreTxt, (self.sCord_x, self.sCord_y))
        
        # Note: HealthPoints Max out at 100 and Min at 0
        # rect(screen, (color), (x,y,w,h)
        pygame.draw.rect(self.myScreen, self.hpBarColor,(self.hBar_x + 35, self.hBar_y, healthPoints, self.hBar_height))  
      
        #outline of rectangle
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 34, self.hBar_y),(self.hBar_x + 136, self.hBar_y))
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 34, self.hBar_y),(self.hBar_x + 34, self.hBar_y + self.hBar_height))
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 34, self.hBar_y + self.hBar_height),(self.hBar_x + 136, self.hBar_y + self.hBar_height))
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 136, self.hBar_y),(self.hBar_x + 136, self.hBar_y + self.hBar_height))




