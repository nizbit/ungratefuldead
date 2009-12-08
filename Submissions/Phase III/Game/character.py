"""
Contents:
    Character
    NPC
    Player
"""

import os
import sys
import pygame
from pygame.locals import *

import vector2d
import item
import stateMachine

class Character(object):
    def __init__(self, spriteSheet, sprites, MAX_VELOCITY):
        """
        Set all attributes of the character class according to the input 
        arguments, and the remaining attributes to default values
        """
        
        #----Images----
        self._spriteSheet = spriteSheet
        
        #----Rects----
        self._spriteSheetRect = self._spriteSheet.get_rect()
        self._rect = pygame.Rect(0,0,0,0)
        self._spriteSheetCoord = pygame.Rect(0,0,0,0)
        
        self._sprites = sprites
        
        #----Stats----
        self._velocity = vector2d.Vector2D(0,0)
        self._HP = 100
        self._lives = 5
        
        self.MAX_VELOCITY = MAX_VELOCITY
        self.attacking = False
        self._direction = "right"
    def setSpriteSheet(self, spriteSheet):
        """
        Set class variable __spriteSheet to spriteSheet
        """
        self._spriteSheet = spriteSheet
    
    def getSpriteSheet(self):
        """
        Return class variable __spriteSheet
        """
        return self._spriteSheet
    
    def setRect(self, rect):
        """
        
        ***NOTE***
        RECT MAY NEED TO BE PUBLIC IF WE WANT TO USE GROUPS
        **********
        
        Set the class variable, __rect, to rect
        """
        print rect
        self._rect = rect
        
    def getRect(self):
        """
        
        ***NOTE***
        RECT MAY NEED TO BE PUBLIC IF WE WANT TO USE GROUPS
        **********
        
        Return the class variable, __rect
        """
        return self._rect
    rect = property(getRect, setRect)
    
    def setPosition(self, x, y):
        self._rect.top = y
        self._rect.left = x
        
    def setSpriteSheetCoord(self, rect):
        """
        Set __spriteSheetCoord to input argument, rect
        """
        self._spriteSheetCoord = rect
        self._rect.w = self._spriteSheetCoord.w
        self._rect.h = self._spriteSheetCoord.h
    
    def getSpriteSheetCoord(self):
        """
        Return __spriteSheetCoord
        """
        return self._spriteSheetCoord
    
    def setVelocity(self, v):
        """
        Set __velocity to argument, velocity
        """
        self._velocity = v
    
    def getVelocity(self):
        """
        Return __velocity
        """
        return self._velocity
    
    velocity = property(getVelocity,setVelocity)
    
    def setHP(self, life):
        """
        Set __HP to life
        """
        self._HP = life
    
    def getHP(self):
        """
        Return __HP
        """
        return self._HP
    
    HP = property(getHP, setHP)
    
    def setDirection(self, direction):
        """
        set __direction equal to direction
        """
        self._direction = direction
    
    def getDirection(self):
        """
        Return __direction
        """
        return self._direction
    
    def changeDirection(self):
        """
        Change the direction of the character. i.e. if the character's
        direction was == to left, then change it to right. Vice Verse.
        """
        if self._direction == "left":
            self._direction = "right"
        else:
            self._direction = "left"
    
    def addSprite(self, key, sprite):
        """
        Add new key and rect to __sprites
        """
        self._sprites[key] = sprite
    
    def getSprite(self, key):
        """
        Return rect based on key argument that corresponds to an element in 
        __sprites
        """
        return self._sprites[key]
    
    def setLives(self, numLives):
        """
        Set __lives to numLives
        """
        self._lives = numLives
    
    def getLives(self):
        """
        Return __lives
        """
        return self._lives
    
    lives = property(getLives,setLives)
    
    def setStateMachine(self, stateMachine):
        """
        Set __stateMachine to stateMachine
        """
        self._stateMachine = stateMachine
    
    def getStateMachine(self):
        return self._stateMachine
    
    def update(self):
        """
        This method will be overridden by its derived classes. The update
        method will change a character's rect, HP, lives, etc. 
        """
        pass
    
    def render(self, surface):
        '''jdb: update this to handle the proj images or override in player ==> no call proj render '''
        surface.blit(self._spriteSheet, self._spriteSheetRect, self._spriteSheetCoord)
    
    def handleCollision(self, type, collideable):
        self._stateMachine.handleCollision(type, collideable)
        
class Player(Character):
    
    def __init__(self, spriteSheet, sprites, MAX_VELOCITY):
        """
        
        ***NOTE***
        WE NEED TO ADD THE PARAMETERS TO THE DOCUMENTATION
        **********
        
        Call the base class' __init__. Set weapons to empty dictionary. Set
        current weapon to none
        """
        super(Player, self).__init__(spriteSheet, sprites, MAX_VELOCITY)

        # Images for the currentWeapon box

        gun1Image = pygame.image.load("Images/weaponPic/handGun.png")
        gun2Image = pygame.image.load("Images/weaponPic/M16.png")
        testImage = pygame.image.load("Images/weaponPic/shotGun.png")

        gun1Image = pygame.image.load("Images/weaponPic/handGun.png")
        gun2Image = pygame.image.load("Images/weaponPic/M16.png")
        gun3Image = pygame.image.load("Images/weaponPic/shotGun.png")
        gun4Image = pygame.image.load("Images/weaponPic/bazooka.png")        
        gun5Image = pygame.image.load("Images/weaponPic/riffleSniper.png")

                
       # gun1Projectile = item.Projectile(gun1Image, self._rect, "testProjectile", None, vector2d.Vector2D(1, 8))
        
        projectileImage1 = pygame.image.load("Images/weaponPic/blackBullet.png")
        projectileImage2 = pygame.image.load("Images/weaponPic/gun1.png")
        projectileImage3 = pygame.image.load("Images/bullet1.png")
        
        
        gun1 = item.Weapon(gun1Image, self._rect, "pistol", None, None, projectileImage1, 30, 11, 10, 10)
        gun2 = item.Weapon(gun2Image, self._rect, "machine", None, None, projectileImage1, 48, 10, 20, 20)
        gun3 = item.Weapon(gun3Image, self._rect, "shotGun", None, None, projectileImage1, 35, 10, 50, 30)
        gun4 = item.Weapon(gun4Image, self._rect, "bazooka", None, None, projectileImage1, 48, 10, 100, 50)
        gun5 = item.Weapon(gun5Image, self._rect, "snipe", None, None, projectileImage1, 80, 0, 100, 30)

        self._safetyNetImage = pygame.image.load("Images/safetyNetPic2.png").convert_alpha()
            
        safetyNet1 = item.Powerups(self._safetyNetImage, self._rect, "safetyNet", None)    
        
        
        self._reloadBool = False
        
        self._powerupList = []
        self._powerupList.append(safetyNet1)
        self._currentPowerup = safetyNet1
        
        self._weaponsList = []
        self._weaponsList.append(gun1)
        self._weaponsList.append(gun2)
        self._weaponsList.append(gun3)
        self._weaponsList.append(gun4)
        self._weaponsList.append(gun5)
        
        
        self._currentWeapon = gun1
                
        self._stateMachine = stateMachine.PlayerStateMachine(self, sprites)
    def setCurrentWeapon(self, name):
        for weapon in self._weaponsList:
            if weapon.getName() == name:
                self._currentWeapon = weapon
    
    def setReloadBool(self, value):
        self._reloadBool = value
        
    def getReloadBool(self):
        return self._reloadBool
    
    def getSafetyNetImage(self):
        return self._safetyNetImage
    def getCurrentPowerup(self):
        return self._currentPowerup
    
    def getWeaponsList(self):
        return self._weaponsList
    
    def setNextWeapon(self):
        
        index = self._weaponsList.index(self._currentWeapon)
        index += 1
        if index < len(self._weaponsList):
            self._currentWeapon = self._weaponsList[index]
        else:
            self._currentWeapon = self._weaponsList[0]
    
    def setPreviousWeapon(self):
        
        index = self._weaponsList.index(self._currentWeapon)
        index -= 1
        if index >= 0:
            self._currentWeapon = self._weaponsList[index]
        else:
            self._currentWeapon = self._weaponsList[len(self._weaponsList) -1]
        
    def getCurrentWeapon(self):
        """
        Return __currentWeapon
        """
        return self._currentWeapon
    
    def addWeapon(self, weapon):
        """
        Add weapon and through key to the weapons dictionary
        """
        self._weaponsList.append(weapon)
    
    def removeWeapon(self, weapon):
        """
        Delete weapon from the weapons dictionary using the key
        """
        self._weaponsList.remove(weapon)
    
    def update(self, event):
        self._stateMachine.handleEvent(event)
        self._stateMachine.handleAnimation()
        self._stateMachine.move()
        
class NPC(Character):
    def __init__(self, spriteSheet, sprites, MAX_VELOCITY, playerRect, topographyRects):
                 
        """
        Call base class' __init__. Set class variables to corresponding
        arguments. Call loadSpeech(speechFile).
        """
        super(NPC, self).__init__(spriteSheet, sprites, MAX_VELOCITY)
        self._stateMachine = stateMachine.EnemyStateMachine(self, sprites, \
                                                            playerRect, topographyRects)
        self.playerRect = playerRect
        self.topographyRects = topographyRects[:]
    def getCopy(self):
        return NPC(self._spriteSheet, self._sprites, self.MAX_VELOCITY, \
                   self.playerRect, self.topographyRects)
    def setItem(self,item):
        """
        Set __item to item.
        
        self._item = item
        """
        pass
    def getItem(self):
        """
        Return __item
        
        return self.__item
        """
        pass
    def update(self, rect):
        self._stateMachine.think(rect)
        self._stateMachine.handleAnimation()
        self._stateMachine.move()
        
if __name__ == "__main__":
    while(True):
        pygame.init()
        screen = pygame.display.set_mode((640,480))
        spriteSheet = pygame.image.load('Images/GR-Zombie.png')
        action = {"right": (15, 15, 35, 45),              
                   "left": (265, 20, 35, 45),
                   "right-run1": (15, 70, 35, 45),
                   "right-run2": (60, 70, 35, 45),
                   "right-run3": (100, 70, 35, 45),
                   "right-run4": (135, 70, 35, 45),
                   "right-run5": (175, 70, 35, 45),
                   "right-run6": (225, 70, 35, 45),
                   "left-run1": (265, 70, 26, 45),
                   "left-run2": (298, 70, 26, 45),
                   "left-run3": (330, 70, 26, 45),
                   "left-run4": (360, 70, 26, 45),
                   "left-run5": (395, 59, 26, 45),
                   "left-run6": (433, 59, 32, 45),
                   "right-attack1": (15, 130, 22, 45),
                   "right-attack2": (52, 130, 44, 45),
                   "right-attack3": (100, 130, 50, 45),
                   "right-attack4": (160, 130, 67, 45),
                   "right-attack5": (238, 130, 42, 45),
                   "right-attack6": (295, 130, 76, 45),
                   "left-attack1": (577, 73, 22, 45),
                   "left-attack2": (526, 62, 44, 45),
                   "left-attack3": (471, 62, 50, 45),
                   "left-attack4": (508, 121, 67, 45),
                   "left-attack5": (459, 120, 42, 45),
                   "left-attack6": (377, 127, 76, 45), }
        actions = {"right": {"right": pygame.Rect(856,70,41,53)},
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
        velocity = vector2d.Vector2D(5,15)
        
        
        platform  = pygame.Rect(0,400, 600,50)
        platform2 = pygame.Rect(100,300, 50,50)
        platform3  = pygame.Rect(100,100, 50,50)
        
        platform5 = pygame.Rect(200,100, 50,50)
        platform6 = pygame.Rect(300,300, 50,100)
        platform7 = pygame.Rect(300,100, 50,50)
        platform8 = pygame.Rect(400,100, 50,50)
        platform9 = pygame.Rect(100,350, 50,50)
        platform10 = pygame.Rect(100,100, 50,50)
        pList = [platform,    
                 platform2,
                 platform3,
                 platform5,
                 platform6,
                 platform7,
                 platform8,
                 platform9,
                 platform10]
        
        platform4 = pygame.Rect(200,300, 50,50)
        enemy = pygame.Surface((50,50))
        enemy.fill((55,55,55))
        temp = pygame.Surface((640,480))
        temp.fill((255,255,255))
        
        #player = NPC(spriteSheet, actions, velocity, "blah", "a", platform4, pList, "b")
        #player.HP = 5
        player = Player(spriteSheet, actions, velocity)
        
        
                
        player.setSpriteSheetCoord(actions["right"]["right"])
        player.setPosition(50,200)
        projectileList = []   
        clock = pygame.time.Clock()
        buf = 11
        running = True
        while(running):
            player.update(pygame.event.get())
            for platform in pList:
                if player.getRect().colliderect(platform):
                    player.handleCollision("object", platform)
            if player.getRect().colliderect(platform4):
                player.handleCollision("enemy", platform4)
            if player.getStateMachine().getCurrentStates().has_key("attack"):
                bulletSound = pygame.mixer.Sound("Sounds/hit.wav")
                bulletSound.set_volume(.25)
                bulletImage = pygame.image.load("Images/bulletTest.png").convert_alpha()
                bulletRect = bulletImage.get_rect()
                bulletVelocity = vector2d.Vector2D(1,1)
                bullet = item.Projectile(bulletImage,bulletRect,"bullet",bulletSound,bulletVelocity,1,1)
                projectileList.append(bullet)
            
            player.getStateMachine().handleAnimation()
            
            clock.tick(60)
            screen.fill((100,100,0))
            #print len(projectileList)
            for bullet in projectileList:
                bullet.update()
                screen.blit(bullet.getImage(),bullet.getRect())
            for p in pList:
                screen.blit(temp,p,p)
            screen.blit(enemy,platform4)
            screen.blit(spriteSheet, player.getRect(), player.getSpriteSheetCoord())
            pygame.display.flip()
            running = True
            
            