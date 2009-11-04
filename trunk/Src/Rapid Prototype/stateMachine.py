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
        #self.__currentState = states.State(character)
        self._currentState = self._standingState
        
        self._actions = {}
        
    def getCurrentState(self):
        return self._currentState
    
    def handleAnimation(self):
        """
        Checks __character's dictionary of sprites and cycles through the
        dictionary with each call
        """
        if self._actions.has_key("attack"):
            for state in self._actions:
                if self._actions[state].__str__() != "AttackingState":
                    self._actions[state].setFrameNum(0)
                    
            temp = self._actions["attack"].getFrame("right")
            temp = self._sprites["attack-right"][temp]
            self._character.setSpriteSheetCoord(temp)   
        #return self._currentState.getFrame()
    
    def handleCollision(self, type, thing):
        """
        Sets __currentState based on collisionBoundary which would be either
        "character", "item", or "solids" and changes the state accordingly. The
        new state's act() method is then called.
        """
        if type == "platform":
            if self._actions.has_key("falling"):
                del self._actions["falling"]
                self._character.velocity.y = 0
            
        
    def noEvent(self):
        """
        """
        if self._currentState == self._standingState:
            pass
        elif self._currentState == self._runningState:
            self._currentState.act()
                
        elif self._currentState == self._jumpingState:
            if self._character.velocity.y == 0:
                self._currentState = self._fallingState
            self._currentState.act()
        elif self._currentState == self._fallingState:
            self._currentState.act()
        
    
class PlayerStateMachine(StateMachine):
    def __init__(self, character, sprites):
        """
        Call the parent class' __init__
        """
        super(PlayerStateMachine, self).__init__(character, sprites)
    
    def handleEvent(self, events):
        """
        Based on the event, set currentState and call act()
        """
        
        if events == []:
            self.noEvent()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self._character.setDirection("right")
                    self._actions["right"] = self._runningState
                    
                if event.key == pygame.K_LEFT:
                    self._character.setDirection("left")
                    self._actions["left"] = self._runningState
                        
                elif event.key == pygame.K_SPACE:
                    if not self._actions.has_key("falling"):
                        self._actions["jump"] = self._jumpingState
                elif event.key == pygame.K_LSHIFT:
                    self._actions["attack"] = self._attackingState
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    del self._actions["right"]
                elif event.key == pygame.K_LEFT:
                    del self._actions["left"]
                #elif event.key == pygame.K_SPACE:
                #    del self._actions["space"]
                elif event.key == pygame.K_LSHIFT:
                    self._actions["attack"].setFrameNum(0)
                    self.handleAnimation()
                    del self._actions["attack"]
        for item in self._actions.items():
            if item[0] == "jump" and \
            self._character.velocity.y == 0:
                del self._actions["jump"]
                self._actions["falling"] = self._fallingState
            item[1].act()
        #print self._currentState
    
class EnemyStateMachine(StateMachine):
    def __init__(self, character, sprites):
        """
        
        ***NOTE***
        WE MIGHT NEED TO RECIEVE ALL THE RECT'S FROM THE WORLD CLASS AS AN
        ARGUMENT
        **********
        
        Call the parent class' __init__
        """
        super(EnemyStateMachine, self).__init__(character, sprites)
    
    def think(self):
        """
        Based on the character's type, currentState, and level topography,
        change currentState to a different state
        """
        pass

if __name__ == "__main__":
    pass