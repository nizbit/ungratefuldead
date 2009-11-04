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
        self.velocity = vector2d.Vector2D(0,0)
        self._HP = 100
        self._lives = 5
        
        self.MAX_VELOCITY = MAX_VELOCITY
        
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
        self._rect.topleft = rect
    def getRect(self):
        """
        
        ***NOTE***
        RECT MAY NEED TO BE PUBLIC IF WE WANT TO USE GROUPS
        **********
        
        Return the class variable, __rect
        """
        return self._rect
    
    def setSpriteSheetCoord(self, rect):
        """
        Set __spriteSheetCoord to input argument, rect
        """
        self._spriteSheetCoord = rect
    
    def getSpriteSheetCoord(self):
        """
        Return __spriteSheetCoord
        """
        return self._spriteSheetCoord
    
    def setVelocity(self, velocity):
        """
        Set __velocity to argument, velocity
        """
        self._velocity = velocity
    
    def getVelocity(self):
        """
        Return __velocity
        """
        return self.velocity
    
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
    
    def setStateMachine(self, stateMachine):
        """
        Set __stateMachine to stateMachine
        """
        self._stateMachine = stateMachine
    def update(self):
        """
        This method will be overridden by its derived classes. The update
        method will change a character's rect, HP, lives, etc. 
        """
        pass
    
    def render(self, surface):
        surface.blit(self._spriteSheet, self._spriteSheetRect, self._spriteSheetCoord)
    
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
        self.__weapons = {}
        self.__currentWeapon = None
        self.__stateMachine = stateMachine.PlayerStateMachine(self)
    def getCurrentWeapon(self):
        """
        Return __currentWeapon
        """
        return self.__currentWeapon
    
    def setCurrentWeapon(self, key):
        """
        set __currentWeapon to the value corresponding to key in __weapons
        """
        self.__currentWeapon = self.__weapons[key]
    
    def addWeapon(self,key, weapon):
        """
        Add weapon and through key to the weapons dictionary
        """
        self.__weapons[key] = weapon
    
    def removeWeapon(self, key):
        """
        Delete weapon from the weapons dictionary using the key
        """
        del self.__weapons[key]
    
    def update(self):
        self.__stateMachine.handleEvent(pygame.event.get())
        
class NPC(Character):
    def __init__(self, spriteSheet, sprites, MAX_VELOCITY, type, speechFile, item):
                 
        """
        Call base class' __init__. Set class variables to corresponding
        arguments. Call loadSpeech(speechFile).
        """
        super(NPC, self).__init__(spriteSheet, sprites, MAX_VELOCITY, \
                                  stateMachine)
        self.__type = type
        self.__item = item
        self.file = None
        self.loadSpeech(speechFile)
        self.__stateMachine = stateMachine.EnemyStateMachine(self)
    def loadSpeech(self, speechFile):
        """
        Load textual information from given argument file name. If the file
        fails to load, throw an exception
        """
        try:
            self.file = open(speechFile, r)
        except IOError:
            print "Could not open file. Exiting program"
            sys.exit()
        
    
    def getType(self):
        """
        Return __type
        """
        return self.__type
    
    def setItem(self,item):
        """
        Set __item to item.
        """
        self.__item = item
    
    def getItem(self):
        """
        Return __item
        """
        return self.__item
    
    def update(self):
        self.__stateMachine.think()
        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    spriteSheet = pygame.image.load('Images/johnmorris.png')
    actions = {"right": (15, 15, 35, 45),              
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
    velocity = vector2d.Vector2D(5,10)
    player = Player(spriteSheet, actions, velocity)
    player.setSpriteSheetCoord(actions["right"])
    player.setRect((0,400))
    clock = pygame.time.Clock()
    while(1):
        player.update()
        clock.tick(50)
        screen.fill((0,0,0))
        screen.blit(spriteSheet, player.getRect(), player.getSpriteSheetCoord())
        pygame.display.flip()