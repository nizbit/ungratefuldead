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
    def __init__(self, character):
        """
        Sets __character to the passed argument character. Create instances of
        all states to be used and assign those states to class variables. Set
        __currentState to the standing state
        """
        '''current character context'''
        self._character = character
        
        '''initialize all states fields'''
        self._standingState = states.StandingState(character)
        self._runningState = states.RunningState(character)
        self._jumpingState = states.JumpingState(character)
        self._fallingState = states.FallingState(character)
        self._attackingState = states.AttackingState(character)
        self._powerupState = states.PowerupState(character)
        self._deadState = states.DeadState(character)
        self._talkingState = states.TalkingState(character)
        
        '''initialize current state to the base class and set to standing'''
        #self.__currentState = states.State(character)
        self._currentState = self._standingState
    def handleAnimation(self):
        """
        Checks __character's dictionary of sprites and cycles through the
        dictionary with each call
        """
        return self._currentState.getFrame()
    
    def handleCollision(self, collisionBoundary):
        """
        Sets __currentState based on collisionBoundary which would be either
        "character", "item", or "solids" and changes the state accordingly. The
        new state's act() method is then called.
        """
        pass
    
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
        elif self._currentState == self._fallingState:
            pass
        
    
class PlayerStateMachine(StateMachine):
    def __init__(self, character):
        """
        Call the parent class' __init__
        """
        super(PlayerStateMachine, self).__init__(character)
    
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
                    if self._character.getDirection() == "left":
                        self._character.changeDirection()
                    if self._currentState == self._standingState:
                        
                        self._currentState = self._runningState
                        
                    elif self._currentState == self._jumpingState or \
                    self._currentState == self._fallingState or \
                    self._currentState == self._attackingState or \
                    self._currentState == self._powerupState:
                        temp = self._currentState
                        self._currentState = self._runningState
                        self._currentState.act()
                        self._currentState = temp
                if event.key == pygame.K_LEFT:
                    if self._character.getDirection() == "right":
                        self._character.changeDirection()
                    if self._currentState == self._standingState:
                        
                        self._currentState = self._runningState
                        
                    elif self._currentState == self._jumpingState or \
                    self._currentState == self._fallingState or \
                    self._currentState == self._attackingState or \
                    self._currentState == self._powerupState:
                        temp = self._currentState
                        self._currentState = self._runningState
                        self._currentState.act()
                        self._currentState = temp
                        
                elif event.key == pygame.K_SPACE:
                    if self._currentState != self._jumpingState:
                        self._currentState = self._jumpingState
                elif event.key == pygame.K_LSHIFT:
                    self._currentState = self._attackingState
                    
                self._currentState.act()
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if self._currentState == self._runningState:
                        self._currentState = self._standingState
                elif event.key == pygame.K_LEFT:
                    if self._currentState == self._runningState:
                        self._currentState = self._standingState
                elif event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_f:
                    pass
                elif event.key == pygame.K_SPACE:
                    pass
            print event
        print self._currentState
    
class EnemyStateMachine(StateMachine):
    def __init__(self, character):
        """
        
        ***NOTE***
        WE MIGHT NEED TO RECIEVE ALL THE RECT'S FROM THE WORLD CLASS AS AN
        ARGUMENT
        **********
        
        Call the parent class' __init__
        """
        super(EnemyStateMachine, self).__init__(character)
    
    def think(self):
        """
        Based on the character's type, currentState, and level topography,
        change currentState to a different state
        """
        pass

if __name__ == "__main__":
    pass