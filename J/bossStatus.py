import math
import sys, pygame
from pygame.locals import *


class BossStatus(object):
    def __init__ (self, screen, fontPath):
        
        self.myScreen = screen 
        self.myFont = pygame.font.Font(fontPath,30)
        self.myFontNone = pygame.font.Font(None, 30)
       
        self.font = self.myFont 
        
        self.hCord_x = 5
        self.hCord_y = 450
        
        self.hBar_x = self.hCord_x - 1
        self.hBar_y = self.hCord_y + 2
        self.hBar_height = 17

        self.outLineRectColor = (255,255,255)
        self.hpBarColor = (0,0,255)
        self.labelColor = (255,255,255)
        
        self.jCounter = 0
        
        self.currentHP = -1 
        self.previousHP = -1
        
        self.redFlag = False
        
        self.lGreen = (32,172,44)
        self.lAmber = (225,194,91)
        self.lRed   = (155, 20,20)
        
        self.bossName = "BOSS"        
        self.hpBarColor = self.lGreen
        
    def upDate(self, healthPoints):
        
        self.currentHP = healthPoints

        if healthPoints != self.previousHP:
             # HP Label
            self.nameTxt = self.font.render(self.bossName, 1, self.labelColor)
            self.healthPointTxt = self.font.render("HP:", 1, self.labelColor)
            self.font = self.myFontNone
            self.hpNumTxt = self.font.render(str(healthPoints), 1, self.labelColor)
            self.font = self.myFont

        self.previousHP = healthPoints

    def render(self):
        if self.redFlag:
            if self.jCounter >= 7:
                self.jCounter = 0
            else:
                self.jCounter += .5 
                        
            offSet = math.floor(15 * math.sin(self.jCounter))
            self.lRed = (155 + offSet,20 + offSet,20 + offSet)
        
        if self.currentHP <= 70:
            self.hpBarColor = self.lAmber
            self.redFlag = False
            if self.currentHP <= 40:
                self.hpBarColor = self.lRed
            self.redFlag = True
        else:
            self.hpBarColor = self.lGreen
            self.redFlag = False  
        
        self.myScreen.blit(self.nameTxt, (self.hCord_x, self.hCord_y - 20))
        # HP
        self.myScreen.blit(self.healthPointTxt, (self.hCord_x, self.hCord_y))
        pygame.draw.rect(self.myScreen, self.hpBarColor,(self.hBar_x + 35, self.hBar_y, self.currentHP * 2, self.hBar_height))
        self.myScreen.blit(self.hpNumTxt, (self.hCord_x + 140, self.hCord_y + 3))

        #outline of rectangle
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 34, self.hBar_y),((self.hBar_x + 136) * 2, self.hBar_y))
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 34, self.hBar_y),(self.hBar_x + 34, self.hBar_y + self.hBar_height))
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 34, self.hBar_y + self.hBar_height),((self.hBar_x + 136) * 2, self.hBar_y + self.hBar_height))
        pygame.draw.line(self.myScreen, self.outLineRectColor, ((self.hBar_x + 136) * 2, self.hBar_y),((self.hBar_x + 136) * 2, self.hBar_y + self.hBar_height))

        



