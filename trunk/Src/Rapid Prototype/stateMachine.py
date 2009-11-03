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

class StateMachine(Object):
    def __init__(self, character):
        """
        Sets __character to the passed argument character. Create instances of
        all states to be used and assign those states to class variables. Set
        __currentState to the standing state
        """
        pass
    
    def handleAnimation(self):
        """
        Checks __character's dictionary of sprites and cycles through the
        dictionary with each call
        """
        pass
    
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
        pass
    
class PlayerStateMachine(StateMachine):
    def __init__(self, character):
        """
        Call the parent class' __init__
        """
        pass
    
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
        pass
    
    def think(self):
        """
        Based on the character's type, currentState, and level topography,
        change currentState to a different state
        """
        pass