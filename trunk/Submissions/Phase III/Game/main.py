import sys
import os

import pygame
from  pygame.locals import *

import menu
import inGameMenu

import world
import viewport

import character
import vector2d

import status
import loader

class Game(object):
    def __init__(self, level):
        """init pygame and the sound mixer"""
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((640,480))
        pygame.display.set_caption("Ungrateful Dead")
        self.clock = pygame.time.Clock()
        self.loader = loader.Loader()
        
        """init the status bar"""
        self.statusBar = status.Status(self.screen, "Images/youmurdererbb_reg.ttf")
        self.currentWeaponImage = pygame.image.load("Images/currentWeaponTest.png")

        """init the world and the characters"""
        self.player = None
        self.loadPlayer(level)
        
        self.enemies = []
        
        self.level = None
        self.vp = None
        self.loadLevel(level)
        
        #MAY BE OVERKILL
        if level == 0:
            self.tempvp = pygame.image.load("Images/level2.png")
        elif level == 1:
            self.tempvp = pygame.image.load("Images/level3.png")
        else:
            self.tempvp = pygame.image.load("Images/bck.png")
        
        #self.loadEnemies(level)
        
        """
        Images
        """
        self.deadImage = pygame.image.load("Images/dead.png").convert()
        self.gameOverImage = pygame.image.load("Images/gameover.png").convert()
        self.winImage = pygame.image.load("Images/win.png").convert()
        self.coin = pygame.image.load("Images/copperCoin.png").convert_alpha()
        self.coinRect = self.coin.get_rect()
        self.coinRect.top = 200
        self.coinRect.left = 3600
        """
        Sounds
        """
        self.heartSound = pygame.mixer.Sound("Sounds/heart.wav")
        self.hurtSound = pygame.mixer.Sound("Sounds/hit.wav")
        self.killSound = pygame.mixer.Sound("HouseSounds/enemySound.ogg")
        self.coinSound = pygame.mixer.Sound("Sounds/coinSound.wav")
        self.gameOverSound = pygame.mixer.Sound("Sounds/tpirhorns.ogg")
        self.gameOverSound.set_volume(.1)
        self.coinSound.set_volume(.05)
        self.killSound.set_volume(.25)
        self.bckMusic = pygame.mixer.music   
        if level == 0:  
            self.bckMusic.load("HouseSounds/gamesong4.ogg")
            self.bckMusic.set_volume(.15)
            self.bckMusic.play()

        elif level == 1:
            self.bckMusic.load("HouseSounds/gamesong2.ogg")
            self.bckMusic.set_volume(.15)
            self.bckMusic.play()
        
        """
        Text
        """
        self.score = 0
        self.font = pygame.font.Font(None, 30)
        self.winText = self.font.render("We don't have a boss yet, so...YOU WIN!!!", 1, (255,255,255))
        self.gameOverText = self.font.render("GAME OVER", 1, (255,255,255))
        self.HPText = self.font.render("HP: ", 1, (255,255,255))
        
        
        
        
        self.projectileListMain = []
        self.powerUpListMain = []
        
        """
        -----------------------------------------------------------------------
        Spawn
        -----------------------------------------------------------------------
        actions velocity spritesheet position
        spritesheet actions velocity rect worldrect
        self.level.platform
        """
        self.leftSpawnCounter = 0
        self.rightSpawnCounter = 0
        self.topSpawnCounter = 0
        self.spawnIndex = 0
        self.spawnList = []
        
        info = self.loader.loadPlayer("Files/darkheartless.plr")
        actions = info[0]
        velocity = info[1]
        spriteSheet = pygame.image.load(info[2]).convert_alpha()
        temp = character.NPC(spriteSheet, actions, velocity, self.player.rect, self.level.platform[:])
        temp.setSpriteSheetCoord(actions["right"]["right"])
        temp.setPosition(0,0)
        self.spawnList.append(temp)
        """
        Flags
        """
        self.running = True
        self.hackyQuit = False
        self.won = False
    
    def loadLevel(self, level):
        self.bckMusic = pygame.mixer.music
        if level == 0: 
            self.bckMusic.load("HouseSounds/gamesong5.ogg")
            info = self.loader.loadLevel("Files/level2.zom")
            
        elif level == 1:
            self.bckMusic.load("HouseSounds/gamesong4.ogg")
            info = self.loader.loadLevel("Files/level3.zom")
        platform = info[0][:]
        enemyBounds = info[1][:]
        image = info[2]
        self.level = world.World(image,[],platform,enemyBounds)
        self.vp = viewport.Viewport(pygame.Rect(info[4][0], info[4][1], \
                                                640, 480), self.player, \
                                                info[3],
                                                info[4][2], info[4][3], \
                                                info[4][4], info[4][5])
        for enemy in info[5]:
            x = None
            if enemy[0] == "zombie":
                x = self.loader.loadPlayer("Files/zombie.plr")
            elif enemy[0] == "grzombie":
                x = self.loader.loadPlayer("Files/grzombie.plr")
            else:
                x = self.loader.loadPlayer("Files/darkheartless.plr")
            actions = x[0]
            velocity = x[1]
            spriteSheet = pygame.image.load(x[2]).convert_alpha()
            temp = character.NPC(spriteSheet, actions, velocity, self.player.rect, self.level.platform[:])
            temp.setSpriteSheetCoord(actions["right"]["right"])
            temp.setPosition(int(enemy[1]), int(enemy[2]))
            self.enemies.append(temp)
            
    def handleEnemies(self, event):
        pass
    
    def pause(self):
        loop = 1
        menu2 = inGameMenu.InGame('Images/ingamemenu.png','Images/mask.png')
        test = menu2.handle_event()
        
        while loop:
            for e in pygame.event.get():
                if e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                    loop = 0
                elif test == 0:
                    loop = 0
                    self.running = False
                    self.hackyQuit = True
                    self.bckMusic.stop()
                elif test == 1:
                    loop = 0

    def update(self):
            
        #print "player velocity: ", self.player.x_velocity
        
        #======================================================
        for weaponElement in self.player.getWeaponsList():
            for projectile in weaponElement.getProjectileList():
                self.projectileListMain.append(projectile)
                weaponElement.getProjectileList().remove(projectile)
        
        # if it goes outside the viewport
        for projectiles in self.projectileListMain:
            if not self.vp.rect.contains(projectiles.getRect()):
                self.projectileListMain.remove(projectiles)            
        
        for powerUp in self.player.getCurrentPowerup().getPowerupList():
            self.powerUpListMain.append(powerUp)
            self.player.getCurrentPowerup().getPowerupList().remove(powerUp)
            
        
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
                    
        '''fall out of the level'''
        if self.player.rect.top > self.vp.rect.bottom or \
        self.player.rect.bottom < self.vp.rect.top:
            self.player.getStateMachine().kill()
            self.running = False
            self.screen.blit(self.deadImage, self.deadImage.get_rect())
            pygame.display.flip()
            
            for projectile in self.projectileListMain:
                self.projectileListMain.remove(projectile)
            for powerUp in self.powerUpListMain:
                self.powerUpListMain.remove(powerUp)
                print str(powerUp)
            pygame.time.wait(3000)
                      
        else:
            '''update everything associated with the player: weapons, projectiles, rects etc...'''
            self.player.update(temp)
            for projectile in self.projectileListMain:
                projectile.update()
            for powerUp in self.powerUpListMain:
                powerUp.update(self.player.getRect())
  

        
        
        
        killList = []
        for enemy in self.enemies:
            '''check projectiles against enemies'''
            for projectile in self.projectileListMain:
                if projectile.getRect().colliderect(enemy.rect):
                    if enemy.HP > 1:
                        enemy.HP -= 20
                        self.projectileListMain.remove(projectile)
                    else:
                        killList.append(enemy)
                        self.killSound.play()
                        self.score += 100 + self.player.HP + self.player.lives * 100
            # Note: check if safetyNet collides with enemies
            for powerUp in self.powerUpListMain:
                if powerUp.getRect().colliderect(enemy.rect):
                    if enemy.HP > 1:
                        enemy.HP -= 20
                        self.powerUpListMain.remove(powerUp)
                    else:
                        killList.append(enemy)
                        self.killSound.play()
                        self.score += 100 + self.player.HP + self.player.lives * 100
               
            if self.player.rect.colliderect(enemy.rect):
                print "enemy: ", enemy.rect, " ", enemy
                if self.player.HP > 1:
                    self.player.HP -= 1
                else:
                    self.running = False
                    self.screen.blit(self.deadImage, self.deadImage.get_rect())
                    pygame.display.flip()
                    for projectile in self.projectileListMain:
                        self.projectileListMain.remove(projectile)
                    for powerUp in self.powerUpListMain:
                        self.powerUpListMain.remove(powerUp)

                    pygame.time.wait(3000)
                coll = self.player.handleCollision("enemy", enemy.rect)
                self.player.getStateMachine().pushEnemy(enemy, coll)             
                
        for enemy in killList:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
                enemy = None
            
        for enemy in self.enemies:
            enemy.update()
        
        for solid in self.level.solids:
            if self.player.rect.colliderect(solid):
                self.player.handleCollision("object", solid)

        
        for platform in self.level.platform:
            if self.player.rect.colliderect(platform):
                self.player.handleCollision("object", platform)

            for projectiles in self.projectileListMain:
                
                if projectiles.getRect().colliderect(platform):
                    self.projectileListMain.remove(projectiles)
                
                if projectiles.getName() == "shotGunShit":
                    tempx = abs(self.player.rect.centerx - projectiles.getRect().centerx)
                    tempy = abs(self.player.rect.centery - projectiles.getRect().centery)
                    if  tempx > 75 or tempy > 75:
                        self.projectileListMain.remove(projectiles) 


        del killList[:]
        
        for enemy in self.enemies:
            if enemy.rect.top > self.vp.rect.bottom or enemy.rect.bottom < self.vp.rect.top:
                killList.append(enemy)
                
        
        for enemy in killList:
            self.enemies.remove(enemy)
            enemy = None
        
            
        if self.player.rect.colliderect(self.coinRect):
            self.won = True
            self.coinSound.play()
            self.screen.blit(self.winText, (100,200))
            pygame.display.flip()
            pygame.time.wait(2000)
            self.screen.blit(self.winImage, self.winImage.get_rect())
            pygame.display.flip()
            pygame.time.wait(3000)
            self.running = False
            
        self.vp.update()
        
        
        if self.running == False:
            self.reset()
        self.statusBar.upDate(self.player.HP, self.score, self.player.lives, self.player.getCurrentWeapon().getImage()) 

        """
        *
        *
        Random Spawn of enemies
        *
        *
        """
        """
        self.leftSpawnCounter += 1
        self.rightSpawnCounter += 1
        self.topSpawnCounter += 1
        if len(self.enemies) < 6:
            if self.rightSpawnCounter > 127:
                self.rightSpawnCounter = 0
                if self.spawnIndex < len(self.spawnList):
                    temp = self.spawnList[self.spawnIndex].getCopy()
                    temp.changeDirection()
                    temp.rect.size = (50,50)
                    temp.setPosition(self.vp.rect.right, self.vp.rect.top)
                    temp.getStateMachine().handleAnimation()
                    self.enemies.append(temp)
                    self.spawnIndex += 1
                else:
                    self.spawnIndex = 0
            if self.leftSpawnCounter > 227:
                self.leftSpawnCounter = 0
                if self.spawnIndex < len(self.spawnList):
                    temp = self.spawnList[self.spawnIndex].getCopy()
                    temp.changeDirection()
                    temp.rect.size = (50,50)
                    temp.setPosition(self.vp.rect.left, self.vp.rect.top)
                    temp.getStateMachine().handleAnimation()
                    self.enemies.append(temp)
                    self.spawnIndex += 1
                else:
                    self.spawnIndex = 0
        """
    def render(self):
        #print "vp: ", self.vp.getViewportSize()
        #print self.viewport
        if self.running:
            self.level.image.blit(self.tempvp,self.vp.rect,self.vp.rect)
            
            
            if self.player.getDirection() == "left":

                #temp = pygame.Surface(self.player.rect.size)
                #temp.blit(self.level.image,self.player.rect)
                #temp.blit(temp,self.player.rect)
                #temp = pygame.transform.flip(temp, True, False)
                #temp.blit(self.player.getSpriteSheet(),(0,0),self.player.getSpriteSheetCoord())
                #temp = pygame.transform.flip(temp, True, False)
                #self.level.image.blit(temp, self.player.rect)
                sprite = pygame.transform.flip(self.player.getSpriteSheet().subsurface(self.player.getSpriteSheetCoord()), True, False)
                self.level.image.blit(sprite,self.player.rect)
            else:
                self.level.image.blit(self.player.getSpriteSheet(),self.player.rect,self.player.getSpriteSheetCoord())
            
            '''blit the projectiles'''
            for projectile in self.projectileListMain:
                self.level.image.blit(projectile.getImage(), projectile.getRect())
                
            for powerUp in self.powerUpListMain:
                self.level.image.blit(powerUp.getImage(), powerUp.getRect())

            if self.vp.rect.inflate(50,0).contains(self.coinRect):
                self.level.image.blit(self.coin,self.coinRect)
            for enemy in self.enemies:
                if self.vp.rect.inflate(50,50).contains(enemy.rect):
                #print enemy.getSpriteSheetCoord()
                    self.level.image.blit(enemy.getSpriteSheet(),enemy.rect,enemy.getSpriteSheetCoord())
            
            self.screen.blit(self.level.image.subsurface(self.vp.rect),(0,0))        
            
            
            self.statusBar.render()
            
            if self.player.HP <= 0:
               self.statusBar.upDate(self.player.HP, self.score, self.player.lives, self.currentWeaponImage)
               self.screen.blit(self.gameOverText, (250,250))
            """
            for x in self.spawnList:
                self.screen.blit(x.getSpriteSheet(),x.rect, x.getSpriteSheetCoord())   
            """
            pygame.display.flip()
            
        
    def run(self):
        self.running = True
        while self.running:
            
            #print event
            """handle the events and animation"""
                     
            self.update()
            self.render()
            self.clock.tick(60)
    def reset(self):
        self.bckMusic.stop()
        if self.won:
            pass
        
        elif self.player.lives > 1 and not self.hackyQuit:
            self.player.HP = 100
            self.player.lives -= 1
            if self.player.getStateMachine().getCurrentStates().has_key("dead"):
                del self.player.getStateMachine().getCurrentStates()["dead"]
                
            """BIG PROBLEM"""
            self.player.setPosition(90, 700)
            self.vp.rect.left = 0
            self.running = True
            
            self.bckMusic.play()
        else:
            self.gameOverSound.play()
            self.screen.blit(self.gameOverImage, self.gameOverImage.get_rect())
            pygame.display.flip()
            pygame.time.wait(3000)
                    
    def loadPlayer(self, level):
        info = self.loader.loadPlayer("Files/lupin.plr")
        actions = info[0]
        velocity = info[1]
        spriteSheet = pygame.image.load(info[2]).convert_alpha()
        self.player = character.Player(spriteSheet, actions, velocity)
        self.player.setSpriteSheetCoord(actions["right"]["right"])
        if level == 1:
            self.player.setPosition(250,684)
        else:
            self.player.setPosition(50, 200)
                        
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