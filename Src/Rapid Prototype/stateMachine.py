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
        self._attackingState = states.AttackingState(character, sprites["attack-right"].keys(),\
                                                   sprites["attack-left"].keys())
        self._powerupState = states.PowerupState(character, sprites["right"].keys(),\
                                                   sprites["left"].keys())
        self._deadState = states.DeadState(character, sprites["right"].keys(),\
                                                   sprites["left"].keys())
        self._talkingState = states.TalkingState(character, sprites["right"].keys(),\
                                                   sprites["left"].keys())
        
        '''initialize current state to the base class and set to standing'''
                
        self._actions = {"falling": self._fallingState}
        self.isJumping = False
    def getCurrentState(self):
        return self._currentState
    
    def handleAnimation(self):
        """
        Checks __character's dictionary of sprites and cycles through the
        dictionary with each call
        """
        
        if self._character.getDirection() == "right":
            if self._actions.has_key("attack"):
                for state in self._actions:
                    if self._actions[state].__str__() != "AttackingState":
                        self._actions[state].resetFrames()
                        
                temp = self._actions["attack"].getFrame("right")
                temp = self._sprites["attack-right"][temp]
                self._character.setSpriteSheetCoord(temp)
            elif self._actions.has_key("runRight"):
                for state in self._actions:
                    if self._actions[state].__str__() != "RunningState":
                        self._actions[state].resetFrames()
                temp = self._actions["runRight"].getFrame("right")
                temp = self._sprites["run-right"][temp]
                self._character.setSpriteSheetCoord(temp)
        else:
            
            if self._actions.has_key("attack"):
                for state in self._actions:
                    if self._actions[state].__str__() != "AttackingState":
                        self._actions[state].resetFrames()
                        
                temp = self._actions["attack"].getFrame("left")
                temp2 = self._sprites["attack-left"][temp]
                self._character.setSpriteSheetCoord(temp2)
                
            elif self._actions.has_key("runLeft"):
                for state in self._actions:
                    if self._actions[state].__str__() != "RunningState":
                        self._actions[state].resetFrames()
                temp = self._actions["runLeft"].getFrame("left")
                temp = self._sprites["run-left"][temp]
                self._character.setSpriteSheetCoord(temp)
        if len(self._actions.keys()) == 1 and self._actions.has_key("falling"):
            for state in self._actions:
                self._actions[state].resetFrames()
            
            if self._character.getDirection() == "right":
                self._actions["right"] = self._standingState
                temp = self._actions["right"].getFrame("right")
                temp = self._sprites["right"][temp]
                self._character.setSpriteSheetCoord(temp)
                del self._actions["right"]
            else:
                self._actions["left"] = self._standingState
                temp = self._actions["left"].getFrame("left")
                temp = self._sprites["left"][temp]
                self._character.setSpriteSheetCoord(temp)
                del self._actions["left"]
                    
    def handleCollision(self, type, rect):
        pass
                  
    def translate(self, rect):
        typeOfColl = None
        bottom = self._character.getRect().bottom - rect.top
        top = self._character.getRect().top - rect.bottom
        
        right = self._character.getRect().right - rect.left
        left = self._character.getRect().left - rect.right
        
        miny = bottom
        
        minx = left
        
        if abs(bottom) > abs(top):
            miny = top
        if abs(left) > abs(right):
            minx = right
        if abs(miny) > abs(minx):
            if abs(left) < abs(right):
                self._character.getRect().left = rect.right
                typeOfColl = "left"
            else:
                self._character.getRect().right = rect.left
                typeOfColl = "right"
            self._character.velocity.x = 0
            
        else:
            if abs(bottom) < abs(top):
                self._character.getRect().bottom = rect.top
                self.isJumping = False
                typeOfColl = "bottom"
            else:
                self._character.getRect().top = rect.bottom
                typeOfColl = "top"
            self._character.velocity.y = 0      
        return typeOfColl
    def act(self):
        for item in self._actions.items():
            item[1].act()
                
        if self._actions.has_key("jump"):
            del self._actions["jump"]
            
            
    def move(self):
        self._character.getRect().left += self._character.velocity.x
        self._character.getRect().top += self._character.velocity.y
    
class PlayerStateMachine(StateMachine):
    def __init__(self, character, sprites):
        """
        Call the parent class' __init__
        """
        super(PlayerStateMachine, self).__init__(character, sprites)
    
    
    def handleCollision(self, type, rect):
        """
        Sets __currentState based on collisionBoundary which would be either
        "character", "item", or "solids" and changes the state accordingly. The
        new state's act() method is then called.
        """
        if type == "object":
            self.translate(rect)
        if type == "enemy":
            self.translate(rect)
            if self._character.HP >= 1:
                self._character.HP -= 1
                print self._character.HP
            else:
                if self._character.lives >= 1:
                    self._character.lives -= 1
                print "DEAD!" 
    
    def handleEvent(self, events):
        """
        Based on the event, set currentState and call act(). Variation of the
        Jon Lutes Algorithm.
        """

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self._actions.has_key("right"):
                        del self._actions["right"]
                    if self._actions.has_key("left"):
                        del self._actions["left"]
                    if self._actions.has_key("runLeft"):
                        del self._actions["runLeft"]
                                             
                    self._character.setDirection("right")
                    self._actions["runRight"] = self._runningState
                    
                if event.key == pygame.K_LEFT:
                    if self._actions.has_key("right"):
                        del self._actions["right"]
                    if self._actions.has_key("left"):
                        del self._actions["left"]
                    if self._actions.has_key("runRight"):
                        del self._actions["runRight"]
                    self._character.setDirection("left")
                    self._actions["runLeft"] = self._runningState
                        
                elif event.key == pygame.K_SPACE:
                    if not self.isJumping:
                        self._actions["jump"] = self._jumpingState
                        self.isJumping = True

                elif event.key == pygame.K_LSHIFT:
                    self._actions["attack"] = self._attackingState
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if self._actions.has_key("runRight"):
                        del self._actions["runRight"]
                    if self._character.getDirection() == "right":
                        self._character.velocity.x = 0
                    #self._actions["right"] = self._standingState
                elif event.key == pygame.K_LEFT:
                    if self._actions.has_key("runLeft"):
                        del self._actions["runLeft"]
                    if self._character.getDirection() == "left":
                        self._character.velocity.x = 0
                    #self._actions["left"] = self._standingState
                #elif event.key == pygame.K_SPACE:
                #    del self._actions["space"]
                elif event.key == pygame.K_LSHIFT:
                    self._actions["attack"].resetFrames()
                    self.handleAnimation()
                    del self._actions["attack"]
        self.act()
    
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
        self._actions["runRight"] = self._runningState
        self.counter = 0
    def handleCollision(self, type, rect):
        if type == "object":
            self.counter += 1
            if self.counter % 17 == 0:
                self._actions["jump"] = self._jumpingState
            typeOfColl = self.translate(rect)
            if typeOfColl == "right" or typeOfColl == "left":
                self.turnAround()
                
        if type == "enemy":
            self.counter += 1
            if self._character.HP >= 1:
                self._character.HP -= 1
            else:
                self._actions.clear()
                self._actions["falling"] = self._fallingState
                self._actions["dead"] = self._deadState

            typeOfColl = self.translate(rect)
            if typeOfColl == "right" or typeOfColl == "left":
                self.turnAround()
                
    def turnAround(self):
        if self._character.getDirection() == "right":
            self._character.setDirection("left")
            if self._actions.has_key("runRight"):
                del self._actions["runRight"]
            self._actions["runLeft"] = self._runningState
        else:
            self._character.setDirection("right")
            if self._actions.has_key("runLeft"):
                del self._actions["runLeft"]
            self._actions["runRight"] = self._runningState
        self._character.velocity.x = 0
        
    def think(self):
        """
        Based on the character's type, currentState, and level topography,
        change currentState to a different state
        """
        for state in self._actions:
            self._actions[state].act()
        if self._actions.has_key("jump"):
            del self._actions["jump"]
        
        
if __name__ == "__main__":
    pass