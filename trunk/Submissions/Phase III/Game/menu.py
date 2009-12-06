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
        self.textShow = []
        self.y = 1200
        self.x = 0
        self.clock = pygame.time.Clock()
        self.fonty = pygame.font.Font('Images/youmurdererbb_reg.ttf', 30)
        self.credText = ['terd burglar','Ungrateful Dead','by','Doug','Chris','David','Jon']
        self.cred = pygame.image.load('Images/creds.png')
        
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
                    elif event.key == pygame.K_F1:
                        self.displayCredits()
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
    
    def displayCredits(self):
        
        self.screen.fill((0,0,0))
        #for text in self.credText:
        #    self.textShow.append(self.fonty.render(text, 1, (123,30,30)))
        #for stuff in self.textShow:
        #    run = True    
        #    while run:
        #        self.x = (640 - stuff.get_width()) / 2
        #        self.y -= 5
        #        if self.y < -stuff.get_height():
        #            self.y = 480
        #            run = False
        #        self.screen.blit(stuff, (self.x,self.y))
        #        pygame.display.flip()
        #            
        #        self.screen.fill((0,0,0))
        #        self.clock.tick(10)
                #run = False
        while self.y > -2000:
            pygame.time.wait(10)
            self.screen.blit(self.cred, (0,self.y))
            pygame.display.flip()
            self.y -= 1
        
        
        
        
        #pygame.time.wait(10000)
            #run = False