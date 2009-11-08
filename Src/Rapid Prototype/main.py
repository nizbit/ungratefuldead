import pygame
import character
import phantom
import world
import viewport
import coin
import sys
import menu
import vector2d
from  pygame.locals import *

class Game(object):
    def __init__(self):
        """init pygame and the sound mixer"""
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((640,480))
        pygame.display.set_caption("Rapid Prototype")
        self.clock = pygame.time.Clock()
        
        """init the world and the characters"""
        self.level = world.World()
        self.vp = viewport.Viewport(pygame.Rect(0,0,640,480))
        #MAY BE OVERKILL
        self.tempvp = pygame.image.load("Images/bck.png")
        self.player = None
        self.loadPlayer()
        
        """
        Sounds
        """
        self.heartSound = pygame.mixer.Sound("Sounds/heart.wav")
        self.hurtSound = pygame.mixer.Sound("Sounds/hit.wav")
        self.killSound = pygame.mixer.Sound("Sounds/killSound.wav")
        self.coinSound = pygame.mixer.Sound("Sounds/coinSound.wav")
        self.coinSound.set_volume(.05)
        self.killSound.set_volume(.25)
        self.bckMusic = pygame.mixer.music 
        self.bckMusic.load("Sounds/music.ogg")
        self.bckMusic.set_volume(.25)
        self.bckMusic.play()
        
        """
        Text
        """
        self.score = 0
        self.font = pygame.font.Font(None, 30)
        self.winText = self.font.render("YOU WIN!!!", 1, (255,255,255))
        self.gameOverText = self.font.render("GAME OVER", 1, (255,255,255))
        self.HPText = self.font.render("HP: ", 1, (255,255,255))
        self.scoreText = self.font.render("Score: ", 1, (255,255,255))
        self.running = True
        
    def handleEnemies(self, event):
        pass
    
    def pause(self):
        loop = 1
        menu2 = menu.menu('Images/menu.png','Images/com.png')
        test = menu2.handle_event()
        
        while loop:
            for e in pygame.event.get():
                if e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                    loop = 0
                elif test == 0:
                    loop = 0
                    self.running = False

    def update(self):

        #print "player velocity: ", self.player.x_velocity
        if self.player.getRect().left >= self.vp.rect.right - 300 and \
        self.player.getRect().left + 300 <= 3800:
            self.vp.rect.right += self.player.velocity.x#self.player.getRect().left + 300
        if self.player.getRect().right <= self.vp.rect.left + 300 and \
        self.player.getRect().right - 300 >= 0:
            self.vp.rect.left += self.player.velocity.x#self.player.getRect().right - 300
        if self.vp.rect.right > 3800:
            self.vp.rect.right = 3800
        if self.vp.rect.left < 0:
            self.vp.rect.left = 0
        
        """loop through the events"""
        temp = pygame.event.get()
        for event in temp:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_ESCAPE:
                    self.pause()
                
                    
        self.player.update(temp)
        if self.player.getRect().colliderect(self.level.solids):
            self.player.handleCollision("object", self.level.solids)
        
        for platform in self.level.platform:
            if self.player.getRect().colliderect(platform):
                self.player.handleCollision("object", platform)
            
    def render(self):
        #print "vp: ", self.vp.getViewportSize()
        #print self.viewport
        self.level.image.blit(self.tempvp,self.vp.rect,self.vp.rect)
        self.level.image.blit(self.player.getSpriteSheet(),self.player.getRect(),self.player.getSpriteSheetCoord())
        
        self.screen.blit(self.level.image.subsurface(self.vp.rect),(0,0))        
        if self.player.HP <= 0:
            self.screen.blit(self.HPText, (0,0))
            self.tempText = self.font.render(str(self.player.HP),1, (255,255,255))
            self.screen.blit(self.tempText, (125, 0))
            
            self.screen.blit(self.scoreText, (0,25))
            self.tempText = self.font.render(str(self.score), 1, (255,255,255))
            self.screen.blit(self.tempText, (75, 25))
            
            self.screen.blit(self.gameOverText, (250,250))
        else:
            self.screen.blit(self.HPText, (0,0))
            self.tempText = self.font.render(str(self.player.HP),1, (255,255,255))
            self.screen.blit(self.tempText, (50, 0))
            
            self.screen.blit(self.scoreText, (0,25))
            self.tempText = self.font.render(str(self.score), 1, (255,255,255))
            self.screen.blit(self.tempText, (75, 25))
        
        pygame.display.flip()
        
        
    def run(self):
        self.running = True
        while self.running:
            
            #print event
            """handle the events and animation"""
                     
            self.update()
            self.render()
            self.clock.tick(60)
            
    def loadPlayer(self):
        actions = {"right": {"right": pygame.Rect(15, 15, 35, 45)},
                  "left": {"left": pygame.Rect(265, 20, 35, 45)},
                  "run-right": {"right-run1": pygame.Rect(15, 70, 35, 45),
                                "right-run2": pygame.Rect(60, 70, 35, 45),
                                "right-run3": pygame.Rect(100, 70, 35, 45),
                                "right-run4": pygame.Rect(135, 70, 35, 45),
                                "right-run5": pygame.Rect(175, 70, 35, 45),
                                "right-run6": pygame.Rect(225, 70, 35, 45)},
                  "run-left": {"left-run1": pygame.Rect(265, 70, 26, 45),
                               "left-run2": pygame.Rect(298, 70, 26, 45),
                               "left-run3": pygame.Rect(330, 70, 26, 45),
                               "left-run4": pygame.Rect(360, 70, 26, 45),
                               "left-run5": pygame.Rect(395, 59, 26, 45),
                               "left-run6": pygame.Rect(433, 59, 32, 45)},
                  "attack-right": {"right-attack1": pygame.Rect(15, 130, 22, 45),
                                   "right-attack2": pygame.Rect(52, 130, 44, 45),
                                   "right-attack3": pygame.Rect(100, 130, 50, 45),
                                   "right-attack4": pygame.Rect(160, 130, 67, 45),
                                   "right-attack5": pygame.Rect(238, 130, 42, 45),
                                   "right-attack6": pygame.Rect(295, 130, 76, 45)},
                  "attack-left": {"left-attack1": pygame.Rect(577, 73, 22, 45),
                                  "left-attack2": pygame.Rect(526, 62, 44, 45),
                                  "left-attack3": pygame.Rect(471, 62, 50, 45),
                                  "left-attack4": pygame.Rect(508, 121, 67, 45),
                                  "left-attack5": pygame.Rect(459, 120, 42, 45),
                                  "left-attack6": pygame.Rect(377, 127, 76, 45)}}
        velocity = vector2d.Vector2D(5,15)
        spriteSheet = pygame.image.load('Images/johnmorris.png')
        self.player = character.Player(spriteSheet, actions, velocity)
        self.player.setSpriteSheetCoord(actions["right"]["right"])
        self.player.setRect((50,200))
        
if __name__ == "__main__":
    while True:
        pygame.init()
        menu1 = menu.menu('Images/menu.png','Images/com.png')
        print "this is where you call level1 for 1 and level2 for 2 and quit the game if 0 " 
        test = menu1.handle_event()
        if test == 1:
            game = Game()
            game.run()
        elif test == 0:
            sys.exit(0)
            