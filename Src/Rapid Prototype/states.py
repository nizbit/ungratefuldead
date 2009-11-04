"""
Contents:
    State
    StandingState
    RunningState
    JumpingState
    FallingState
    AttackingState
    DeadState
    TalkingState
    PowerupState
"""
import os
import sys
import pygame
from pygame.locals import *

import vector2d
import character

class State(object):
    """
    This is the base class for all states.
    """
    def __init__(self, character):
        """
        Set all class variables to their corresponding arguments. With the
        exception of frame, which gets set to zero.
        """
        self._character = character
        
        self.__leftFrames = {}
        self.__rightFrames = {}
        
        self.__frameNum = 0
    
    def getFrame(self, frameSet):
        """
        Return the string that corresponds to a key in the character's sprite
        dictionary to retrieve a frame for animation. __frameNum is used to
        cycle through the appropriate frame set for animation. The frameSet is
        a collection of strings which will be used as keys in the sprite
        dictionary
        """
        self.__frameNum += 1
        if self.__frameNum > (len(frameSet) - 1):
            self.__frameNum = 0
        return frameSet[self.__frameNum]
    
    def getFrameNum(self):
        """
        Return the current frame
        """
        return self.__frameNum
    
    def act(self):
        """
        This method is a pure virtual method to be overridden by derived
        classes. Each state has it's own act method which will be called to
        perform some action on the character  
        """
        pass
    
    def __str__(self):
        return "State"
    
class StandingState(State):
    
    def __init__(self, character):
        """
        Call the base class' constructor
        """
        super(StandingState, self).__init__(character)
        
    def act(self):
        """
        Set the x and y velocity values of the character to zero
        """
        self._character.velocity.x = 0
        self._character.velocity.y = 0

    def __str__(self):
        return "StandingState"

class RunningState(State):
    def __init__(self, character):
        """
        Call the base class' constructor
        """
        super(RunningState, self).__init__(character)
    
    def act(self):
        """
        Increment the x velocity with each call until it reaches MAX_VELOCITY
        """
        
        #self.__character.velocity.x = 0
        if self._character.getDirection() == "right":
            if self._character.velocity.x < 0:
                self._character.velocity.x = 0
            elif self._character.getVelocity().x < \
            self._character.MAX_VELOCITY.x:
                self._character.velocity.x += 1
                
            self._character.getRect().move_ip(self._character.velocity.x, 0)
                
        else:
            if self._character.velocity.x > 0:
                self._character.velocity.x = 0
            elif self._character.getVelocity().x > \
            (-1 * self._character.MAX_VELOCITY.x):
                self._character.velocity.x -= 1
            self._character.getRect().move_ip(self._character.velocity.x, 0)

    def __str__(self):
        return "RunningState"
    
class JumpingState(State):
    def __init__(self, character):
        """
        Call the base class' constructor
        """
        super(JumpingState,self).__init__(character)

    def act(self):
        """
        Set the y velocity to MAX_VELOCITY and with each call, decrement until
        velocity is equal to zero. If the velocity equals zero, no calculations
        need to be performed so do nothing
        """
        if self._character.velocity.y == 0:
            self._character.velocity.y = -1 * self._character.MAX_VELOCITY.y
            
        if self._character.velocity.y < 0:
            self._character.velocity.y += 1
            self._character.getRect().move_ip(0, self._character.velocity.y)
        
             
    def __str__(self):
        return "JumpingState"
    
class FallingState(State):
    def __init__(self, character):
        super(FallingState,self).__init__(character)

    def act(self):
        """
        Increment y velocity with each call until velocity is equal to 
        MAX_VELOCITY. If the velocity equals MAX_VELOCITY, no calculations need
        to be performed so do nothing
        """
        if self._character.velocity.y < self._character.MAX_VELOCITY.y:
            self._character.velocity.y += 1
        self._character.getRect().move_ip(0, self._character.velocity.y)
    def __str__(self):
        return "FallingState"
class AttackingState(State):
    def __init__(self, character):
        super(AttackingState,self).__init__(character)
    
    def act(self):
        """
        Inject projectile into the world, based upon the current type of
        weapon
        """
        pass
    
    def __str__(self):
        return "AttackingState"
    
class DeadState(State):
    def __init__(self, character):
        super(DeadState,self).__init__(character)
    
    def act(self):
        """
        Take away a character life. Set x and y velocity to zero
        """
        pass
    
    def __str__(self):
        return "DeadState"
    
class TalkingState(State):
    def __init__(self, character):
        super(TalkingState,self).__init__(character)
    
    def act(self):
        """
        Will set the x and y velocity values to zero. Initiate dialog string
        from dialogFile.txt
        """
        pass
    
    def __str__(self):
        return "TalkingState"
    
class PowerupState(State):
    def __init__(self, character):
        super(PowerupState,self).__init__(character)
    
    def act(self):
        """
        Apply effects of a powerup to the character
        """
        pass
    
    def __str__(self):
        return "PowerupState"

        
