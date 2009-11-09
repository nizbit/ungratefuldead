import pygame
import character
import phantom
import world
import viewport
import coin
import sys
import menu
import vector2d
import inGameMenu
from  pygame.locals import *

class Game(object):
    def __init__(self, level):
        """init pygame and the sound mixer"""
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((640,480))
        pygame.display.set_caption("Rapid Prototype")
        self.clock = pygame.time.Clock()
        
        """init the world and the characters"""
        self.level = None
        self.loadLevel(level)
        self.vp = viewport.Viewport(pygame.Rect(0,0,640,480))
        #MAY BE OVERKILL
        if level == 0:
            self.tempvp = pygame.image.load("Images/level2.png")
        else:
            self.tempvp = pygame.image.load("Images/bck.png")
        self.player = None
        self.loadPlayer()
        
        self.enemies = []
        self.loadEnemies(level)
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
    
    def loadLevel(self, level):
        if level == 0:
            solids = [pygame.Rect(0, 0, 10, 480),
                      pygame.Rect(3790, 0, 10, 480),
                      pygame.Rect(0, 103, 3800, 10),
                      pygame.Rect(0, 367, 925, 113),
                      pygame.Rect(1144, 367, 770, 113),
                      pygame.Rect(2190, 367, 423, 113),
                      pygame.Rect(2715, 367, 56, 113),
                      pygame.Rect(2892, 367, 908, 113)]
        
            platform = [pygame.Rect(333, 343,117, 24),
                        pygame.Rect(450, 289,116, 78),
                        pygame.Rect(1518, 294,226, 73),
                        pygame.Rect(1869, 244, 118, 23),
                        pygame.Rect(2141, 244,118, 23),
                        pygame.Rect(2487, 288, 116, 78),
                        pygame.Rect(2994,244, 118,23)]
            
            self.level = world.World("Images/level2.png", solids, platform)
        else:
            solids = [pygame.Rect(0, 0, 3800, 10),
                      pygame.Rect(0, 470, 3800, 10),
                      pygame.Rect(0, 0, 10, 470),
                      pygame.Rect(3790, 0, 10, 470)]
        
            platform = [pygame.Rect(410, 398,100, 20),
                        pygame.Rect(540, 382,100, 20),
                        pygame.Rect(934, 408,100, 20),
                        pygame.Rect(1450, 405,100, 20),
                        pygame.Rect(1573, 377,100, 20),
                        pygame.Rect(1705, 371,100, 20),
                        pygame.Rect(2605, 407, 100, 20),
                        pygame.Rect(2605,362, 100, 20),
                        pygame.Rect(2605,319, 100, 20),
                        pygame.Rect(2605,274, 100, 20),
                        pygame.Rect(2605,223, 100, 20),
                        pygame.Rect(2605,168, 100, 20),
                        pygame.Rect(3161,192, 100, 20),
                        pygame.Rect(3290,245, 100, 20),
                        pygame.Rect(3295,372, 100, 20),
                        pygame.Rect(3420,296, 100, 20),
                        pygame.Rect(3550,343, 100, 20)]
            self.level = world.World("Images/bck.png", solids, platform)    
    def handleEnemies(self, event):
        pass
    
    def pause(self):
        loop = 1
        menu2 = inGameMenu.InGame('Images/ingamemenu.png','Images/dink.png')
        test = menu2.handle_event()
        
        while loop:
            for e in pygame.event.get():
                if e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                    loop = 0
                elif test == 0:
                    loop = 0
                    self.running = False
                elif test == 1:
                    loop = 0

    def update(self):

        #print "player velocity: ", self.player.x_velocity
        
        
        """loop through the events"""
        temp = pygame.event.get()
        for event in temp:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_ESCAPE:
                    self.bckMusic.pause()
                    self.pause()
                    self.bckMusic.unpause()
                
                    
        self.player.update(temp)
        for solid in self.level.solids:
            if self.player.getRect().colliderect(solid):
                self.player.handleCollision("object", solid)
        
        for platform in self.level.platform:
            if self.player.getRect().colliderect(platform):
                self.player.handleCollision("object", platform)
        for enemy in self.enemies:
            enemy.update()
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
                
    def render(self):
        #print "vp: ", self.vp.getViewportSize()
        #print self.viewport
        self.level.image.blit(self.tempvp,self.vp.rect,self.vp.rect)
        
        self.level.image.blit(self.player.getSpriteSheet(),self.player.getRect(),self.player.getSpriteSheetCoord())
        
        for enemy in self.enemies:
            if self.vp.rect.inflate(50,50).contains(enemy.getRect()):
            #print enemy.getSpriteSheetCoord()
                self.level.image.blit(enemy.getSpriteSheet(),enemy.getRect(),enemy.getSpriteSheetCoord())
        
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
                  "run-left": {"left-run6": pygame.Rect(433, 59, 32, 45),
                               "left-run5": pygame.Rect(395, 59, 26, 45),
                               "left-run4": pygame.Rect(360, 70, 26, 45),
                               "left-run3": pygame.Rect(330, 70, 26, 45),
                               "left-run2": pygame.Rect(298, 70, 26, 45),
                               "left-run1": pygame.Rect(265, 70, 26, 45)},
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
        velocity = vector2d.Vector2D(4,12)
        spriteSheet = pygame.image.load('Images/johnmorris.png').convert_alpha()
        self.player = character.Player(spriteSheet, actions, velocity)
        self.player.setSpriteSheetCoord(actions["right"]["right"])
        self.player.setPosition(50,300)
        
    def loadEnemies(self, level):
        zombieSpriteSheet = pygame.image.load('Images/zombie.png').convert_alpha()
        zombieActions = {"right": {"right": pygame.Rect(120, 4, 40, 80)},
                  "left": {"left": pygame.Rect(838, 5, 40, 80)},
                  "run-right": {"right-run1": pygame.Rect(163, 4, 45, 76),
                                "right-run2": pygame.Rect(208, 4, 45, 76),
                                "right-run3": pygame.Rect(257, 4, 50, 76),
                                "right-run4": pygame.Rect(314, 4, 45, 76),
                                "right-run5": pygame.Rect(365, 4, 40, 76),
                                "right-run6": pygame.Rect(405, 4, 40, 76),
                                "right-run7": pygame.Rect(450, 4, 40, 76)},
                  "run-left": {"left-run1": pygame.Rect(793, 7, 45, 76),
                               "left-run2": pygame.Rect(745, 7, 45, 76),
                               "left-run3": pygame.Rect(688, 7, 50, 76),
                               "left-run4": pygame.Rect(636, 7, 45, 76),
                               "left-run5": pygame.Rect(594, 7, 40, 76),
                               "left-run6": pygame.Rect(551, 7, 40, 76),
                               "left-run7": pygame.Rect(508, 7, 40, 76)},
                  "attack-right": {"right": pygame.Rect(120, 4, 40, 80)},
                  "attack-left": {"left": pygame.Rect(838, 5, 40, 80)}}
        zombieVelocity = vector2d.Vector2D(3,5)
        
        zombieSpriteSheet2 = pygame.image.load('Images/GR-Zombie.png').convert_alpha()
        zombieActions2 = {"right": {"right": pygame.Rect(856,70,41,53)},
                           "left" : {"left": pygame.Rect(264,70,41,53)},
                           "run-right": {"right-run1": pygame.Rect(589,138,40,50),
                                         "right-run2": pygame.Rect(639,138,50,51),
                                         "right-run3": pygame.Rect(702,138,46,51),
                                         "right-run4": pygame.Rect(766,138,42,51),
                                         "right-run5": pygame.Rect(822,138,33,52),
                                         "right-run6": pygame.Rect(869,138,43,51),
                                         "right-run7": pygame.Rect(923,138,48,50),
                                         "right-run8": pygame.Rect(981,138,48,53),
                                         "right-run9": pygame.Rect(1044,138,41,53),
                                         "right-run10": pygame.Rect(1104,138,38,51)},
                           "run-left": {"left-run1": pygame.Rect(523,138,40,50),
                                         "left-run2": pygame.Rect(461,138,50,51),
                                         "left-run3": pygame.Rect(403,138,46,51),
                                         "left-run4": pygame.Rect(345,138,42,51),
                                         "left-run5": pygame.Rect(296,138,33,52),
                                         "left-run6": pygame.Rect(240,138,43,51),
                                         "left-run7": pygame.Rect(180,138,48,50),
                                         "left-run8": pygame.Rect(122,138,48,53),
                                         "left-run9": pygame.Rect(66,138,41,53),
                                         "left-run10": pygame.Rect(9,138,38,51)},
                           "attack-right": {"right-attack": pygame.Rect(813, 342, 32, 53),
                                            "right-attack2": pygame.Rect(861, 342, 31, 54),
                                            "right-attack3": pygame.Rect(914, 342, 32, 51),
                                            "right-attack4": pygame.Rect(967,349,46,47),
                                            "right-attack5": pygame.Rect(1028,353,51,43),
                                            "right-attack6": pygame.Rect(1092,356,53,40)},
                           "attack-left":{"left-attack": pygame.Rect(307, 342,32,53),
                                          "left-attack2": pygame.Rect(259, 342,31,54),
                                          "left-attack3": pygame.Rect(203, 342,32,51),
                                          "left-attack4": pygame.Rect(139, 349,46,47),
                                          "left-attack5": pygame.Rect(73, 353,51,43),
                                          "left-attack6": pygame.Rect(7, 355 ,53,40)}}
        zombieVelocity2 = vector2d.Vector2D(3,5)
        tempRect = pygame.Rect(0,0,0,0)
        tempWorldRects = []
        
        for platform in self.level.solids:
            tempWorldRects.append(platform)
        for platform in self.level.platform:
            tempWorldRects.append(platform)
            
        for x in range(0,10,1):
            self.enemies.append(character.NPC(zombieSpriteSheet,
                                              zombieActions,
                                              zombieVelocity,
                                              "blah",
                                              "a",
                                              self.player.getRect(),
                                              tempWorldRects,
                                              "a"))
            #self.enemies[x].setSpriteSheetCoord(zombieActions["right"]["right"])
        for x in range(11,21,1):
            self.enemies.append(character.NPC(zombieSpriteSheet2, 
                                              zombieActions2, 
                                              zombieVelocity2, 
                                              "blah",
                                              "a", 
                                              self.player.getRect(),
                                              tempWorldRects, 
                                             "a"))
            #self.enemies[x].setSpriteSheetCoord(zombieActions2["right"]["right"])
        
        for x in range(0,10,1):
            self.enemies[x].setSpriteSheetCoord(zombieActions["right"]["right"])
        for x in range(10,20,1):
            self.enemies[x].setSpriteSheetCoord(zombieActions2["right"]["right"])
            
        if self.level == 0:
            self.enemies[0].setPosition(50,300)
            self.enemies[1].setPosition(388,340)
            self.enemies[2].setPosition(752,368)
            self.enemies[3].setPosition(788,352)
            self.enemies[4].setPosition(1294,296)
            self.enemies[5].setPosition(1400,352)
            self.enemies[6].setPosition(1544,294)
            self.enemies[7].setPosition(1600,276)
            self.enemies[8].setPosition(1672,276)
            self.enemies[9].setPosition(1924,240)
            self.enemies[10].setPosition(2204,240)
            self.enemies[11].setPosition(2248,368)
            self.enemies[12].setPosition(2300,368)
            self.enemies[13].setPosition(2508,288)
            self.enemies[14].setPosition(2576,288)
            self.enemies[15].setPosition(2948,360)
            self.enemies[16].setPosition(3056,240)
            self.enemies[17].setPosition(3056,360)
            self.enemies[18].setPosition(3100,360)
            self.enemies[19].setPosition(3200,360)
            #self.enemies[21].setPosition(3300,360)
            #self.enemies[22].setPosition(3400,360)
            
        else:
            self.enemies[0].setPosition(460,352)
            self.enemies[1].setPosition(592,376)
            self.enemies[2].setPosition(960,390)
            self.enemies[3].setPosition(1500,390)
            self.enemies[4].setPosition(1620,372)
            self.enemies[5].setPosition(504,276)
            self.enemies[6].setPosition(3596,324)
            self.enemies[7].setPosition(3660,368)
            self.enemies[8].setPosition(972,450)
            self.enemies[9].setPosition(1020,450)
            self.enemies[10].setPosition(1100,450)
            self.enemies[11].setPosition(1250,450)
            self.enemies[12].setPosition(2000,450)
            self.enemies[13].setPosition(2200,450)
            self.enemies[14].setPosition(2450,450)
            self.enemies[15].setPosition(2600,450)
            self.enemies[16].setPosition(2750,450)
            self.enemies[17].setPosition(2800,450)
            self.enemies[18].setPosition(3000,450)
            self.enemies[19].setPosition(3300,450)
            #self.enemies[21].setPosition(3460,450)
            #self.enemies[22].setPosition(3530,450)
            for enemy in self.enemies:
                print enemy.getRect()
                
if __name__ == "__main__":
    while True:
        pygame.init()
        menu1 = menu.Menu('Images/menu.png','Images/com.png')
        #print "this is where you call level1 for 1 and level2 for 2 and quit the game if 0 " 
        test = menu1.handle_event()
        if test == 2:
            game = Game(1)
            game.run()
        elif test == 1:
            game = Game(0)
            game.run()
        elif test == 0:
            sys.exit(0)    