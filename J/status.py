import sys, pygame
from pygame.locals import *


class Status(object):
    def __init__ (self, screen, healthPoints, score, lives):

        self.font = pygame.font.Font(Arial, 25)
    
        self.hCord_x = 5
        self.hCord_y = 5
    
        self.sCord_x = 5
        self.sCord_y = 35
        
        self.lCord_x = 5
        self.lCord_y = 20
    
        outLineRectColor = (255,0,0)
        hpBarColor = (0,0,255)
        labelColor = (255,255,255)
    
        self.healthPointTxt = self.font.render("HP:", 1, labelColor)
        self.hpNumTxt = self.font.render(str(healthPoints), 1, labelColor)

        self.scoreTxt = self.font.render("Score: " + str(score), 1, labelColor)
        
        self.liveTxt = self.font.render("Lives: " + str(lives), 1, labelColor)
        
        
        # HP Label
        screen.blit(self.healthPointTxt, (self.hCord_x, self.hCord_y))
        # HP Num
        #screen.blit(self.hpNumTxt, (self.hCord_x + 140, self.hCord_y))
        
        # Lives
        screen.blit(self.liveTxt, (self.lCord_x, self.lCord_y))
        # Score
        screen.blit(self.scoreTxt, (self.sCord_x, self.sCord_y))
        
    
        # Note: HealthPoints Max out at 100 and Min at 0
        # rect(screen, (color), (x,y,w,h)
        pygame.draw.rect(screen, hpBarColor,(self.hCord_x + 35, self.hCord_y + 2, healthPoints,12))  
      
      
        #outline of rectangle
        pygame.draw.line(screen, outLineRectColor, (self.hCord_x + 35, self.hCord_y + 2),(self.hCord_x + 135, self.hCord_y + 2))
        pygame.draw.line(screen, outLineRectColor, (self.hCord_x + 35, self.hCord_y + 2),(self.hCord_x + 35, self.hCord_y + 14))
        pygame.draw.line(screen, outLineRectColor, (self.hCord_x + 35, self.hCord_y + 14),(self.hCord_x + 135, self.hCord_y + 14))
        pygame.draw.line(screen, outLineRectColor, (self.hCord_x + 135, self.hCord_y + 2),(self.hCord_x + 135, self.hCord_y + 14))


     



