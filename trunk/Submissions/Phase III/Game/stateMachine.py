"""
Contents:
    StateMachine
    EnemyStateMachine
    PlayerStateMachine
"""
import os
import sys
import pygame
from pygame.locals import *

import vector2d
import character
import states

class StateMachine(object):
    def __init__(self, character, sprites):
        """
        Sets __character to the passed argument character. Create instances of
        all states to be used and assign those states to class variables. Set
        __currentState to the standing state
        """
        '''current character context'''
        self._character = character
        self._sprites = sprites
        '''initialize all states fields'''
        
        self._standingState = states.StandingState(character, sprites["right"].keys(),\
                                                   sprites["left"].keys())
        self._runningState = states.RunningState(character, sprites["run-right"].keys(),\
                                                   sprites["run-left"].keys())
        self._jumpingState = states.JumpingState(character, sprites["right"].keys(),\
                                                   sprites["left"].keys())
        self._fallingState = states.FallingState(character, sprites["right"].keys(),\
                                                   sprites["left"].keys())
        self._attackingState = states.AttackingState(character, sprites["run-right"].keys(),\
                                                   sprites["run-left"].keys())
        self._powerupState = states.PowerupState(character, sprites["right"].keys(),\
                                                   sprites["left"].keys())
        self._deadState = states.DeadState(character, sprites["right"].keys(),\
                                                   sprites["left"].keys())
        self._talkingState = states.TalkingState(character, sprites["right"].keys(),\
                                                   sprites["left"].keys())
        
        '''initialize current state to the base class and set to standing'''
                
        self._currentStates = {"falling": self._fallingState, \
                               "right": self._standingState, \
                               "left": self._standingState}
        self.isJumping = False
        self.isCrouching = False
        self.wallJump = False
        self.wallLeft = False
        self.wallRight = False
        
        self._jCountFromLastPress= 0
        
        
    def getCurrentStates(self):
        return self._currentStates
    def handleAnimation(self):
        """
        Checks __character's dictionary of sprites and cycles through the
        dictionary with each call
        """
        
        if self._character.getDirection() == "right":
            if self._currentStates.has_key("attack"):
                for state in self._currentStates:
                    if self._currentStates[state].__str__() != "AttackingState":
                        self._currentStates[state].resetFrames()
                        
                temp = self._currentStates["attack"].getFrame("right")
                temp = self._sprites["attack-right"][temp]
                self._character.setSpriteSheetCoord(temp)
            elif self._currentStates.has_key("runRight"):
                for state in self._currentStates:
                    if self._currentStates[state].__str__() != "RunningState":
                        self._currentStates[state].resetFrames()
                temp = self._currentStates["runRight"].getFrame("right")
                temp = self._sprites["run-right"][temp]
                self._character.setSpriteSheetCoord(temp)
        else:
            
            if self._currentStates.has_key("attack"):
                for state in self._currentStates:
                    if self._currentStates[state].__str__() != "AttackingState":
                        self._currentStates[state].resetFrames()
                        
                temp = self._currentStates["attack"].getFrame("left")
                temp2 = self._sprites["attack-left"][temp]
                self._character.setSpriteSheetCoord(temp2)
                
            elif self._currentStates.has_key("runLeft"):
                for state in self._currentStates:
                    if self._currentStates[state].__str__() != "RunningState":
                        self._currentStates[state].resetFrames()
                temp = self._currentStates["runLeft"].getFrame("left")
                temp = self._sprites["run-left"][temp]
                self._character.setSpriteSheetCoord(temp)
        if len(self._currentStates.keys()) == 1 and self._currentStates.has_key("falling"):
            for state in self._currentStates:
                self._currentStates[state].resetFrames()
            
            if self._character.getDirection() == "right":
                self._currentStates["right"] = self._standingState
                temp = self._currentStates["right"].getFrame("right")
                temp = self._sprites["right"][temp]
                
                self._character.setSpriteSheetCoord(temp)
                del self._currentStates["right"]
            else:
                self._currentStates["left"] = self._standingState
                temp = self._currentStates["left"].getFrame("left")
                temp = self._sprites["left"][temp]
                self._character.setSpriteSheetCoord(temp)
                del self._currentStates["left"]
    
   
    def handleCollision(self, type, rect):
        pass
                  
    def translate(self, rect):
        typeOfColl = None
        bottom = self._character.rect.bottom - rect.top
        top = self._character.rect.top - rect.bottom
        
        right = self._character.rect.right - rect.left
        left = self._character.rect.left - rect.right
        
        miny = bottom
        
        minx = left
        
        if abs(bottom) > abs(top):
            miny = top
        if abs(left) > abs(right):
            minx = right
        if abs(miny) > abs(minx):
            if abs(left) < abs(right):
                self._character.rect.left = rect.right
                typeOfColl = "left"
            else:
                self._character.rect.right = rect.left
                typeOfColl = "right"
            self.wallJump = True
            self._character.velocity.x = 0
            
        else:
            if abs(bottom) < abs(top):
                self._character.rect.bottom = rect.top
                self.isJumping = False
                self.wallJump = False
                typeOfColl = "bottom"
            else:
                self._character.rect.top = rect.bottom
                typeOfColl = "top"
            self._character.velocity.y = 0      
        return typeOfColl
    
    def act(self):
        for item in self._currentStates.items():
            item[1].act()
                
        if self._currentStates.has_key("jump"):
            del self._currentStates["jump"]
            
    def kill(self):
        
        if self._currentStates.has_key("runRight"):
            del self._currentStates["runRight"]
        if self._currentStates.has_key("runLeft"):
            del self._currentStates["runLeft"]
        self._currentStates["dead"] = self._deadState
                
    def move(self):
        self._character.rect.left += self._character.velocity.x
        self._character.rect.top += self._character.velocity.y
        
class PlayerStateMachine(StateMachine):
    def __init__(self, character, sprites):
        """
        Call the parent class' __init__
        """
        super(PlayerStateMachine, self).__init__(character, sprites)
        self.jumpSound = pygame.mixer.Sound("Sounds/jump.wav")
        
    def handleAnimation(self):
        
        """
        Checks __character's dictionary of sprites and cycles through the
        dictionary with each call
        """
        attackRunKey = []
        attackStandKey = []
        if self._currentStates.has_key("attack"):
            if self._character.getCurrentWeapon().getName() == "pistol":
                self._runningState.rightFrames = self._sprites["pistol-run-right"].keys()
                self._runningState.leftFrames = self._sprites["pistol-run-left"].keys()
                attackRunKey = ["pistol-run-right", "pistol-run-left"]
                
                if self._attackingState.direction == "up":
                    self._standingState.rightFrames = self._sprites["pistol-up-right"].keys()
                    self._standingState.leftFrames = self._sprites["pistol-up-left"].keys()
                    attackStandKey = ["pistol-up-right", "pistol-up-left"]
                
                elif self._attackingState.direction == "down":
                    self._standingState.rightFrames = self._sprites["pistol-down-right"].keys()
                    self._standingState.leftFrames = self._sprites["pistol-down-left"].keys()
                    attackStandKey = ["pistol-down-right", "pistol-down-left"]
                
                else:
                    self._standingState.rightFrames = self._sprites["pistol-right"].keys()
                    self._standingState.leftFrames = self._sprites["pistol-left"].keys()
                    attackStandKey = ["pistol-right", "pistol-left"]
                    
            elif self._character.getCurrentWeapon().getName() == "machine":
                self._runningState.rightFrames = self._sprites["machine-run-right"].keys()
                self._runningState.leftFrames = self._sprites["machine-run-left"].keys()
                attackRunKey = ["machine-run-right", "machine-run-left"]
                
                if self._attackingState.direction == "up":
                    self._standingState.rightFrames = self._sprites["machine-up-right"].keys()
                    self._standingState.leftFrames = self._sprites["machine-up-left"].keys()
                    attackStandKey = ["machine-up-right", "machine-up-left"]
                
                elif self._attackingState.direction == "down":
                    self._standingState.rightFrames = self._sprites["machine-down-right"].keys()
                    self._standingState.leftFrames = self._sprites["machine-down-left"].keys()
                    attackStandKey = ["machine-down-right", "machine-down-left"]
                
                else:
                    self._standingState.rightFrames = self._sprites["machine-right"].keys()
                    self._standingState.leftFrames = self._sprites["machine-left"].keys()
                    attackStandKey = ["machine-right", "machine-left"]
            
            elif self._character.getCurrentWeapon().getName() == "shotGun":
                self._runningState.rightFrames = self._sprites["shot-run-right"].keys()
                self._runningState.leftFrames = self._sprites["shot-run-left"].keys()
                attackRunKey = ["shot-run-right", "shot-run-left"]
            
                if self._attackingState.direction == "up":
                    self._standingState.rightFrames = self._sprites["shot-up-right"].keys()
                    self._standingState.leftFrames = self._sprites["shot-up-left"].keys()
                    attackStandKey = ["shot-up-right", "shot-up-left"]
                
                elif self._attackingState.direction == "down":
                    self._standingState.rightFrames = self._sprites["shot-down-right"].keys()
                    self._standingState.leftFrames = self._sprites["shot-down-left"].keys()
                    attackStandKey = ["shot-down-right", "shot-down-left"]
                
                else:
                    self._standingState.rightFrames = self._sprites["shot-right"].keys()
                    self._standingState.leftFrames = self._sprites["shot-left"].keys()
                    attackStandKey = ["shot-right", "shot-left"]
            
            elif self._character.getCurrentWeapon().getName() == "bazooka":
                attackStandKey = ["bazooka-right", "bazooka-left"]
                attackRunKey = ["bazooka-right", "bazooka-left"]
                self._runningState.rightFrames = self._sprites["bazooka-right"].keys()
                self._runningState.leftFrames = self._sprites["bazooka-left"].keys()
                self._standingState.rightFrames = self._sprites["bazooka-right"].keys()
                self._standingState.leftFrames = self._sprites["bazooka-left"].keys()
            
            else:
                attackStandKey = ["snipe-right", "snipe-left"]
                attackRunKey = ["snipe-right", "snipe-left"]
                self._runningState.rightFrames = self._sprites["snipe-right"].keys()
                self._runningState.leftFrames = self._sprites["snipe-left"].keys()
                self._standingState.rightFrames = self._sprites["snipe-right"].keys()
                self._standingState.leftFrames = self._sprites["snipe-left"].keys()
        
        else:
            """
            NEED TO CHANGE!!!!!!!!!!!!!!!!!!!!!!!!!!!
            """
            if self.isCrouching:
                attackStandKey = ["crawl-right", "crawl-left"]
                attackRunKey = ["crawl-move-right", "crawl-move-left"]
                self._runningState.rightFrames = self._sprites["crawl-move-right"].keys()
                self._runningState.leftFrames = self._sprites["crawl-move-left"].keys()
                self._standingState.rightFrames = self._sprites["crawl-right"].keys()
                self._standingState.leftFrames = self._sprites["crawl-left"].keys()
            else:
                attackStandKey = ["right", "left"]
                attackRunKey = ["run-right", "run-left"]
                self._runningState.rightFrames = self._sprites["run-right"].keys()
                self._runningState.leftFrames = self._sprites["run-left"].keys()
                self._standingState.rightFrames = self._sprites["right"].keys()
                self._standingState.leftFrames = self._sprites["left"].keys()
        
        temp = None
        #print self._character.getCurrentWeapon().getName()
        if self._character.getDirection() == "right":
            if self._currentStates.has_key("runRight"):   
                temp = self._currentStates["runRight"].getFrame("right")
                temp = self._sprites[attackRunKey[0]][temp]
            else:
                temp = self._currentStates["right"].getFrame("right")
                temp = self._sprites[attackStandKey[0]][temp]
            
        else:
            if self._currentStates.has_key("runLeft"):   
                temp = self._currentStates["runLeft"].getFrame("left")
                
                temp = self._sprites[attackRunKey[1]][temp]
            else:
                temp = self._currentStates["left"].getFrame("left")
                temp = self._sprites[attackStandKey[1]][temp]
                    
        self._character.setSpriteSheetCoord(temp)
        
        if len(self._currentStates.keys()) == 1 and self._currentStates.has_key("falling"):
            for state in self._currentStates:
                self._currentStates[state].resetFrames()
            
            if self._character.getDirection() == "right":
                self._currentStates["right"] = self._standingState
                temp = self._currentStates["right"].getFrame("right")
                temp = self._sprites["right"][temp]
                
                self._character.setSpriteSheetCoord(temp)
                del self._currentStates["right"]
            else:
                self._currentStates["right"] = self._standingState
                temp = self._currentStates["right"].getFrame("right")
                temp = self._sprites["right"][temp]
                
                self._character.setSpriteSheetCoord(temp)
                del self._currentStates["right"]
                
                self._currentStates["left"] = self._standingState
                temp = self._currentStates["left"].getFrame("left")
                temp = self._sprites["left"][temp]
                self._character.setSpriteSheetCoord(temp)
                del self._currentStates["left"]
                
    def handleCollision(self, type, rect):
        """
        Sets __currentState based on collisionBoundary which would be either
        "character", "item", or "solids" and changes the state accordingly. The
        new state's act() method is then called.
        """
        coll = "n/a"
        amount = 50
        if type == "object":
            self.translate(rect)
        if type == "enemy":
            
            coll = self.translate(rect)
            if self._character.attacking:
                if coll == "right":
                    rect.left += amount
                elif coll == "left":
                    rect.right -= amount
                elif coll == "top":
                    rect.bottom -= amount
                else:
                    rect.top += amount
        return coll
        """
        if self._character.HP >= 1:
            self._character.HP -= 1
            print self._character.HP
        else:
            if self._character.lives >= 1:
                self._character.lives -= 1
            print "DEAD!" 
        """
    def pushEnemy(self, enemy, direction):
        amount = 150
        
        if direction == "right":
            
            enemy.right += amount
        elif direction == "left":
            
            enemy.left -= amount
        elif direction == "top":
            
            enemy.top -= amount
        elif direction == "bottom":
            
            enemy.bottom += amount
            
    def handleEvent(self, events):
        """
        Based on the event, set currentState and call act(). Variation of the
        Jon Lutes Algorithm.
        """
        self._jCountFromLastPress += 1
        
        if self._jCountFromLastPress <= self._character.getCurrentWeapon().getWait():
            self._character.setReloadBool(True)
        else:
            self._character.setReloadBool(False)
        
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self._character.getCurrentWeapon().getName() != "snipe" and \
                    self._character.getCurrentWeapon().getName() != "bazooka":
                        self._attackingState.direction = "up"
                        
                if event.key == pygame.K_DOWN:
                    if self._character.getCurrentWeapon().getName() != "bazooka":
                        self._attackingState.direction = "down"
                    
                if event.key == pygame.K_RIGHT:
                    self._attackingState.direction = "straight"
                    if (self._character.getCurrentWeapon().getName() == "bazooka" or \
                    self._character.getCurrentWeapon().getName() == "snipe"):
                        if self._character.getDirection() == "left":
                            self._character.changeDirection()
                    else:
                        if self._currentStates.has_key("runLeft"):
                            del self._currentStates["runLeft"]
                                                 
                        self._character.setDirection("right")
                        self._currentStates["runRight"] = self._runningState
                    
                if event.key == pygame.K_LEFT:
                    self._attackingState.direction = "straight"
                    if (self._character.getCurrentWeapon().getName() == "bazooka" or \
                    self._character.getCurrentWeapon().getName() == "snipe"):
                        if self._character.getDirection() == "right":
                            self._character.changeDirection()
                    else:
                        if self._currentStates.has_key("runRight"):
                            del self._currentStates["runRight"]
                        self._character.setDirection("left")
                        self._currentStates["runLeft"] = self._runningState
                        
                elif event.key == pygame.K_SPACE:
                    if not self.isJumping and not self.isCrouching and \
                    self._character.getCurrentWeapon().getName() != "bazooka":
                        self._currentStates["jump"] = self._jumpingState
                        self.isJumping = True
                        self.jumpSound.play()
                    if self.isCrouching:
                        self._character.rect.move_ip(0,50)
                    if self.wallJump and not self.isCrouching:
                        self._character.changeDirection()
                        if self._currentStates.has_key("runRight"):
                            del self._currentStates["runRight"]
                        if self._currentStates.has_key("runLeft"):
                            del self._currentStates["runLeft"]
                        self._currentStates["jump"] = self._jumpingState
                        

                elif event.key == pygame.K_LSHIFT:
                    if self._jCountFromLastPress >= self._character.getCurrentWeapon().getWait():
                        self._jCountFromLastPress = 0
                    
                        self._currentStates["attack"] = self._attackingState
                        
                        
                        
                        
                        if self._character.getCurrentWeapon().getName() == "snipe" and\
                        not self.isCrouching:
                            del self._currentStates["attack"]
# =-==========================================================================================
                elif event.key == pygame.K_1:
                    self._character.setNextWeapon()
                    if "attack" in self._currentStates:
                        self._currentStates["attack"].direction = "straight"
                elif event.key == pygame.K_2:
                    self._character.setPreviousWeapon()
                    if "attack" in self._currentStates:
                        self._currentStates["attack"].direction = "straight"
                elif event.key == pygame.K_z:
                    self.isCrouching = True
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or \
                event.key == pygame.K_DOWN:
                    self._attackingState.direction = "straight"
                if event.key == pygame.K_RIGHT:
                    if self._currentStates.has_key("runRight"):
                        del self._currentStates["runRight"]
                    if self._character.getDirection() == "right":
                        self._character.velocity.x = 0
                    #self._currentStates["right"] = self._standingState
                elif event.key == pygame.K_LEFT:
                    if self._currentStates.has_key("runLeft"):
                        del self._currentStates["runLeft"]
                    if self._character.getDirection() == "left":
                        self._character.velocity.x = 0
                    #self._currentStates["left"] = self._standingState
                #elif event.key == pygame.K_SPACE:
                #    del self._currentStates["space"]
                elif event.key == pygame.K_LSHIFT:
                    if self._currentStates.has_key("attack"):
                        self._currentStates["attack"].resetFrames()
                    self.handleAnimation()
                    if self._currentStates.has_key("attack"):
                        del self._currentStates["attack"]
                    self._character.attacking = False
                elif event.key == pygame.K_z:
                    self.isCrouching = False
        self.act()
        self.wallJump = False
class EnemyStateMachine(StateMachine):
    def __init__(self, character, sprites, playerRect, topographyRects):
        """
        
        ***NOTE***
        WE MIGHT NEED TO RECIEVE ALL THE RECT'S FROM THE WORLD CLASS AS AN
        ARGUMENT
        **********
        
        Call the parent class' __init__
        """
        super(EnemyStateMachine, self).__init__(character, sprites)
        if self._character.getDirection() == "right":
            self._currentStates["runRight"] = self._runningState
        else:
            self._currentStates["runLeft"] = self._runningState
        self._currentStates["falling"] = self._fallingState
        self.counter = 0
        self.tRects = []
        for rect in topographyRects:
            self.tRects.append(rect)
        
    def handleCollision(self, type, rect):
        if type == "object":
            self.counter += 1
            if self.counter % 17 == 0:
                self._currentStates["jump"] = self._jumpingState
            typeOfColl = self.translate(rect)
            if typeOfColl == "right" or typeOfColl == "left":
                self.turnAround()
                
        if type == "enemy":
            self.counter += 1
            if self._character.HP >= 1:
                self._character.HP -= 1
            else:
                self._currentStates.clear()
                self._currentStates["falling"] = self._fallingState
                self._currentStates["dead"] = self._deadState

            typeOfColl = self.translate(rect)
            if typeOfColl == "right" or typeOfColl == "left":
                self.turnAround()
                
    def turnAround(self):
        if self._character.getDirection() == "right":
            self._character.setDirection("left")
            if self._currentStates.has_key("runRight"):
                del self._currentStates["runRight"]
            self._currentStates["runLeft"] = self._runningState
        else:
            self._character.setDirection("right")
            if self._currentStates.has_key("runLeft"):
                del self._currentStates["runLeft"]
            self._currentStates["runRight"] = self._runningState
        self._character.velocity.x = 0
        
    def think(self, rect, vpPlatformList):
        """
        Based on the character's type, currentState, and level topography,
        change currentState to a different state
        """
        sepx = self._character.rect.centerx - rect.centerx
        print sepx
        if sepx > 0:
            if self._character.getDirection() == "right" and \
            "runRight" in self._currentStates:
                
                self.turnAround()
        elif sepx < 0:
            if self._character.getDirection() == "left" and \
            "runLeft" in self._currentStates:
                
                self.turnAround()
        else:
            print "fucker"
                
        for state in self._currentStates:
            self._currentStates[state].act()
        if self._currentStates.has_key("jump"):
            del self._currentStates["jump"]
        for rect in vpPlatformList:
            if self._character.rect.colliderect(rect):
                self.handleCollision("object", rect)
        
#        for rect in self.tRects:
#            print "count me"
#            if self._character.rect.colliderect(rect):
#                self.handleCollision("object", rect)
        
        
if __name__ == "__main__":
    pass