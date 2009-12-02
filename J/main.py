import pygame
import sys
import os
import status

class game(object):
    def __init__(self):
        pygame.init()
        window = pygame.display.set_mode((640, 480))
        
        #pygame.display.toggle_fullscreen()
        pygame.display.set_caption("Hello")
        
        self.screen = pygame.display.get_surface()
        
        self.tempSurface = pygame.Surface((640, 480))
        self.tempSurface.fill((0,0,0))
        
    
        
        self.jImage = pygame.image.load('Images/currentSelection.png')
        
        self.weapon = pygame.image.load('Images/currentWeaponTest.png')
                
        self.clock = pygame.time.Clock()

        
        
        self.font = pygame.font.Font(None, 40)
        self.titleTxt = self.font.render(" Main Menu ", 1, (255,255,255))
        self.startGameTxt = self.font.render(" Start Game ", 1, (255,255,255))
        self.settingsTxt = self.font.render(" Settings ", 1, (255,255,255))
        self.exitTxt = self.font.render(" Exit ", 1, (255,255,255))
        
  
        pygame.key.set_repeat(360, 180)

        self.yCord = 100
        self.xCord = 180

        self.counter = 100
        self.status1 = status.Status(self.screen, "youmurdererbb_reg.ttf")

        self.counter2 = 1

    def upDate(self):
        
        
        self.screen.blit(self.tempSurface, (0, 0))
        
        self.screen.blit(self.jImage, (self.xCord, self.yCord))
        self.screen.blit(self.titleTxt, (200, 100))
        self.screen.blit(self.startGameTxt, (200, 130))
        self.screen.blit(self.settingsTxt, (200, 160))
        self.screen.blit(self.exitTxt, (200, 190))
        
        self.status1.upDate(self.counter,self.counter2, 1,self.weapon)
        
        
    def render(self):
        pygame.display.flip()
        

    def run(self):
        i = 1
        
        if self.counter2 <= 1000000:
            self.counter2 += 100
        else:
            self.counter2 = 1
        
      
        if self.counter >= 1:
            self.counter -= 1
        else:
            self.counter = 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                   sys.exit(0)
                elif event.key == pygame.K_DOWN:
                    self.yCord += 30
                elif event.key == pygame.K_UP:
                    self.yCord -= 30
                else:
                    print(event)
            
            if self.yCord <= 100:
                self.yCord = 190
            if self.yCord >= 220:
                self.yCord = 130
                
                 
        self.upDate()
        self.render()
        self.clock.tick(60)




if __name__ == "__main__":
    what = game()
    while True:
        what.run()
        
        