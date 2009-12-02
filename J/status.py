import math
import sys, pygame
from pygame.locals import *


class Status(object):
    def __init__ (self, screen, fontPath):
        
        self.myScreen = screen 
        self.font = pygame.font.Font(fontPath, 30)

        self.myFont = fontPath

        self.hCord_x = 5
        self.hCord_y = 5
        
        self.hBar_x = self.hCord_x - 1
        self.hBar_y = self.hCord_y + 2
        self.hBar_height = 17
    
        self.sCord_x = 490
        self.sCord_y = 5
        
        self.lCord_x = 5
        self.lCord_y = 25
        
        self.cw_x = 285
        self.cw_y = 5
        
        self.outLineRectColor = (255,255,255)
        self.hpBarColor = (0,0,255)
        self.labelColor = (255,255,255)
        
        self.jCounter = 0;
        
    def upDate(self, healthPoints, score, lives, currentWeapon):
        
     
        #currentWeapon.set_colorkey((255,255,255), RLEACCEL)

        
        healthPoints = 30
        
        if self.jCounter >= 7:
            self.jCounter = 0
        else:
            self.jCounter += .5
        
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
        
       #Max Score : 1000000 length = 7
        
        currentWeaponFrameColor = (232, 132, 24)
            
    
        
        self.healthPointTxt = self.font.render("HP:", 1, self.labelColor)
        self.hpNumTxt = self.font.render(str(healthPoints), 1, self.labelColor)
       
        self.scoreTxt = self.font.render("Score: ", 1, self.labelColor)
        
        self.font = pygame.font.Font(None, 30)
        self.scoreNumTxt = self.font.render(str(score).rjust(7), 1, self.labelColor)
        self.lifeNumTxt = self.font.render(str(lives).rjust(2), 1, self.labelColor)
        self.font = pygame.font.Font(self.myFont, 30)
        
        self.liveTxt  = self.font.render("Lives: ", 1, self.labelColor)    
        

        self.myScreen.blit(currentWeapon, (self.cw_x, self.cw_y))
        
        
        pygame.draw.rect(self.myScreen, currentWeaponFrameColor, (self.cw_x, self.cw_y, 13, 3))
        pygame.draw.rect(self.myScreen, currentWeaponFrameColor, (self.cw_x, self.cw_y, 3, 13))
        
        pygame.draw.rect(self.myScreen, currentWeaponFrameColor, (self.cw_x + 37, self.cw_y, 13, 3))
        pygame.draw.rect(self.myScreen, currentWeaponFrameColor, (self.cw_x + 47, self.cw_y, 3, 13))   
        
        pygame.draw.rect(self.myScreen, currentWeaponFrameColor, (self.cw_x, self.cw_y + 37, 3, 13))
        pygame.draw.rect(self.myScreen, currentWeaponFrameColor, (self.cw_x, self.cw_y + 47, 13, 3))
        
        pygame.draw.rect(self.myScreen, currentWeaponFrameColor, (self.cw_x + 47, self.cw_y + 37, 3, 13))
        pygame.draw.rect(self.myScreen, currentWeaponFrameColor, (self.cw_x + 37, self.cw_y + 47, 13, 3))
        
        
        # HP Label
        self.myScreen.blit(self.healthPointTxt, (self.hCord_x, self.hCord_y))
        # HP Num
        self.myScreen.blit(self.hpNumTxt, (self.hCord_x + 140, self.hCord_y))
        # Lives
        self.myScreen.blit(self.liveTxt, (self.lCord_x, self.lCord_y))
        self.myScreen.blit(self.lifeNumTxt, (self.lCord_x + 50, self.lCord_y + 4))
        # Score
        self.myScreen.blit(self.scoreTxt, (self.sCord_x, self.sCord_y))
        self.myScreen.blit(self.scoreNumTxt, (self.sCord_x + 60, self.sCord_y + 4))
        
        # Note: HealthPoints Max out at 100 and Min at 0
        # rect(screen, (color), (x,y,w,h)
        pygame.draw.rect(self.myScreen, self.hpBarColor,(self.hBar_x + 35, self.hBar_y, healthPoints, self.hBar_height))  
      
        #outline of rectangle
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 34, self.hBar_y),(self.hBar_x + 136, self.hBar_y))
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 34, self.hBar_y),(self.hBar_x + 34, self.hBar_y + self.hBar_height))
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 34, self.hBar_y + self.hBar_height),(self.hBar_x + 136, self.hBar_y + self.hBar_height))
        pygame.draw.line(self.myScreen, self.outLineRectColor, (self.hBar_x + 136, self.hBar_y),(self.hBar_x + 136, self.hBar_y + self.hBar_height))




