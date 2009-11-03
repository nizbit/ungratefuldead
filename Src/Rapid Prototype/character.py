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

import vector2D


class Character(Object):
    def __init__(self, spriteSheet, sprites, MAX_VELOCITY, stateMachine):
        """
        Set all attributes of the character class according to the input 
        arguments, and the remaining attributes to default values
        """
        
        #----Images----
        self.__spriteSheet = spriteSheet
        
        #----Rects----
        self.__spriteSheetRect = self.__spriteSheet.get_rect()
        self.__rect = pygame.Rect(0,0,0,0)
        self.__spriteSheetCoord = pygame.Rect(0,0,0,0)
        
        
        self.__sprites = sprites
        
        #----Stats----
        self.__velocity = Vector2D(0,0)
        self.__HP = 100
        self.__lives = 5
        
        self.__MAX_VELOCITY = MAX_VELOCITY
        self.__stateMachine = stateMachine
    
    def setSpriteSheet(self, spriteSheet):
        """
        Set class variable __spriteSheet to spriteSheet
        """
        self.__spriteSheet = spriteSheet
    
    def getSpriteSheet(self):
        """
        Return class variable __spriteSheet
        """
        return self.__spriteSheet
    
    def setRect(self, levelPosition):
        """
        
        ***NOTE***
        RECT MAY NEED TO BE PUBLIC IF WE WANT TO USE GROUPS
        **********
        
        Set the class variable, __rect, to levelPosition
        """
        self.__rect.topleft = levelPosition
    
    def getRect(self):
        """
        
        ***NOTE***
        RECT MAY NEED TO BE PUBLIC IF WE WANT TO USE GROUPS
        **********
        
        Return the class variable, __rect
        """
        return self.__rect
    
    def setSpriteSheetCoord(self, rect):
        """
        Set __spriteSheetCoord to input argument, rect
        """
        self.__spriteSheetCoord = rect
    
    def getSpriteSheetCoord(self):
        """
        Return __spriteSheetCoord
        """
        return self.__spriteSheetCoord
    
    def setVelocity(self, velocity):
        """
        Set __velocity to argument, velocity
        """
        self.__velocity = velocity
    
    def getVelocity(self):
        """
        Return __velocity
        """
        return self.__velocity
    
    def setHP(self, life):
        """
        Set __HP to life
        """
        self.__HP = life
    
    def getHP(self):
        """
        Return __HP
        """
        return self.__HP
    
    def setDirection(self, direction):
        """
        set __direction equal to direction
        """
        self.__direction = direction
    
    def getDirection(self):
        """
        Return __direction
        """
        return self.__direction
    
    def changeDirection(self):
        """
        Change the direction of the character. i.e. if the character's
        direction was == to left, then change it to right. Vice Verse.
        """
        if self.__direction == "left":
            self.__direction = "right"
        else:
            self.__direction = "left"
    
    def addSprite(self, key, sprite):
        """
        Add new key and rect to __sprites
        """
        self.__sprites[key] = sprite
    
    def getSprite(self, key):
        """
        Return rect based on key argument that corresponds to an element in 
        __sprites
        """
        return self.__sprites[key]
    
    def setLives(self, numLives):
        """
        Set __lives to numLives
        """
        self.__lives = numLives
    
    def getLives(self):
        """
        Return __lives
        """
        return self.__lives
    
    def setStateMachine(self, stateMachine):
        """
        Set __stateMachine to stateMachine
        """
        self.__stateMachine = stateMachine
    
    def update(self):
        """
        This method will be overridden by its derived classes. The update
        method will change a character's rect, HP, lives, etc. 
        """
        pass
    
class Player(Character):
    
    def __init__(self, spriteSheet, sprites, MAX_VELOCITY, stateMachine):
        """
        
        ***NOTE***
        WE NEED TO ADD THE PARAMETERS TO THE DOCUMENTATION
        **********
        
        Call the base class' __init__. Set weapons to empty dictionary. Set
        current weapon to none
        """
        super(Player, self).__init__(spriteSheet, sprites, MAX_VELOCITY, stateMachine)
        self.__weapons = {}
        self.__currentWeapon = None
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
    
class NPC(Character):
    def __init__(self, spriteSheet, sprites, MAX_VELOCITY, stateMachine,\
                 type, speechFile, item):
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
    