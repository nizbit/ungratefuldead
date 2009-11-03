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

import vector2D
import character
import states

class StateMachine(Object):
    def __init__(self, character):
        """
        Sets __character to the passed argument character. Create instances of
        all states to be used and assign those states to class variables. Set
        __currentState to the standing state
        """
        '''current character context'''
        self.__character = character
        
        '''initialize all states fields'''
        self.__standingState = states.StandingState(character)
        self.__runningState = states.RunningState(character)
        self.__jumpingState = states.JumpingState(character)
        self.__fallingState = states.FallingState(character)
        self.__attackingState = states.AttackingState(character)
        self.__powerupState = states.PowerupState(character)
        self.__deadState = states.DeadState(character)
        self.__talkingState = states.TalkingState(character)
        
        '''initialize current state to the base class and set to standing'''
        self.__currentState = states.State(character)
        self.__currentState = self.__standingState
    
    def handleAnimation(self):
        """
        Checks __character's dictionary of sprites and cycles through the
        dictionary with each call
        """
        return self.__currentState.getFrame()
    
    def handleCollision(self, collisionBoundary):
        """
        Sets __currentState based on collisionBoundary which would be either
        "character", "item", or "solids" and changes the state accordingly. The
        new state's act() method is then called.
        """
        pass
    
    def noEvent(self):
        """
        Call the current state's act method
        """
        self.__currentState.act()
    
class PlayerStateMachine(StateMachine):
    def __init__(self, character):
        """
        Call the parent class' __init__
        """
        super(PlayerStateMachine, self).__init__(character)
    
    def handleEvent(self, event):
        """
        Based on the event, set currentState and call act()
        """
        pass
    
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