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
import item
import character

class State(object):
    """
    This is the base class for all states.
    """
    def __init__(self, character, rightFrames, leftFrames):
        """
        Set all class variables to their corresponding arguments. With the
        exception of frame, which gets set to zero.
        """
        self._character = character
        
        self.leftFrames = leftFrames
        self.rightFrames = rightFrames
        
        self._frameNum = 0
        self._counter = 0
        self._jCounter = 0
        self._jCounterPrevious = 0
        
    def getFrame(self, frameSet):
        """
        Return the string that corresponds to a key in the character's sprite
        dictionary to retrieve a frame for animation. __frameNum is used to
        cycle through the appropriate frame set for animation. The frameSet is
        a collection of strings which will be used as keys in the sprite
        dictionary
        """
        self._counter += 1

        if self._counter > 10:
            self._counter = 0
            self._frameNum += 1
        if frameSet == "right":
            if self._frameNum > (len(self.rightFrames) - 1):
                self._frameNum = 0
            return self.rightFrames[self._frameNum]
        else:
            if self._frameNum > (len(self.leftFrames) - 1):
                self._frameNum = 0
            return self.leftFrames[self._frameNum]
    
    def getFrameNum(self):
        """
        Return the current frame
        """
        return self._frameNum
    
    def setFrameNum(self, num):
        self._frameNum = num
    def resetFrames(self):
        self._frameNum = 0
        self._counter = 0
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
    
    def __init__(self, character, rightFrames, leftFrames):
        """
        Call the base class' constructor
        """
        super(StandingState, self).__init__(character, rightFrames, leftFrames)
        
    def act(self):
        """
        Set the x and y velocity values of the character to zero
        """
        pass

    def __str__(self):
        return "StandingState"

class RunningState(State):
    def __init__(self, character, rightFrames, leftFrames):
        """
        Call the base class' constructor
        """
        super(RunningState, self).__init__(character, rightFrames, leftFrames)
    
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
                self._character.velocity.x += .5
                
            #self._character.rect.move_ip(self._character.velocity.x, 0)
                
        else:
            if self._character.velocity.x > 0:
                self._character.velocity.x = 0
            elif self._character.getVelocity().x > \
            (-1 * self._character.MAX_VELOCITY.x):
                self._character.velocity.x -= .5
            #self._character.rect.move_ip(self._character.velocity.x, 0)

    def __str__(self):
        return "RunningState"
    
class JumpingState(State):
    def __init__(self, character, rightFrames, leftFrames):
        """
        Call the base class' constructor
        """
        super(JumpingState,self).__init__(character, rightFrames, leftFrames)
        
    def act(self):
        """
        Set the y velocity to MAX_VELOCITY and with each call, decrement until
        velocity is equal to zero. If the velocity equals zero, no calculations
        need to be performed so do nothing
        """
        #if self._character.velocity.y == 0:
        
        self._character.velocity.y = -1 * self._character.MAX_VELOCITY.y
        #self._character.rect.move_ip(0, self._character.velocity.y)
        """   
        if self._character.velocity.y < 0:
            self._character.velocity.y += .5
        self._character.rect.move_ip(0, self._character.velocity.y)
        """
             
    def __str__(self):
        return "JumpingState"
    
class FallingState(State):
    def __init__(self, character, rightFrames, leftFrames):
        super(FallingState,self).__init__(character, rightFrames, leftFrames)

    def act(self):
        """
        Increment y velocity with each call until velocity is equal to 
        MAX_VELOCITY. If the velocity equals MAX_VELOCITY, no calculations need
        to be performed so do nothing
        """
        
        if self._character.velocity.y < self._character.MAX_VELOCITY.y:
            self._character.velocity.y += .5
        #self._character.rect.move_ip(0, self._character.velocity.y)
    def __str__(self):
        return "FallingState"
    
class AttackingState(State):
    def __init__(self, character, rightFrames, leftFrames):
        super(AttackingState,self).__init__(character, rightFrames, leftFrames)
        self.hurtSound = pygame.mixer.Sound("Sounds/whip.wav")
        self.hurtSound.set_volume(.1)
        self._bulletImage = pygame.image.load('Images/bullets.png')
        self.direction = "straight"
        
    def act(self):
        """
        Inject projectile into the world, based upon the current type of
        weapon
        """
        '''Add a projectile to the list of projectiles'''
        
        '''(basically adding a proj to the world)**This could be a power up ==> take the last two conditions out, it's like hyper mode**'''
        
        # self.direction == up | staight | down
        
        tempProjAngle = 0
        angle = 0 

        tempX = self._character.getCurrentWeapon().getOffsetX()
        tempY = self._character.getCurrentWeapon().getOffsetY()
        
        weaponName = self._character.getCurrentWeapon().getName()
        weaponPower = self._character.getCurrentWeapon().getPower()
        
       # print "Your mother likes it when i touch her here" + str(self._frameNum)
        
        
        #print str(self._character.getDirection()) 
        if self._character.getDirection() == "right":           # right
            tempProjAngle = 0
            #tempY = 35
            if weaponName == "snipe":
                tempY += 10

            if self.direction == "down":        # right and down
                tempProjAngle = 45
                tempY += 25
                if weaponName == "machine":
                    tempProjAngle = 35
                    tempY += 5
                if weaponName == "snipe":
                    tempY -= 25
                    
            
            elif self.direction == "up":                               # right and up
                tempProjAngle = 270
                tempX = 8
                tempY = -2                               
                
                if weaponName == "machine":
                    tempY -= 10
                
                if weaponName == "shotGun":
                    tempY -= 15
                    tempX += 3
            
            
        else:   # left                          # left
            tempProjAngle = 180  
            tempX = 0
            
            if weaponName == "snipe":
                    tempY += 10

            if self.direction == "down":        # left and down
                tempProjAngle = 135
                tempY += 25
                if weaponName == "snipe":
                    tempY -= 25
                if weaponName == "machine":
                    tempProjAngle = 150
                    tempY += 5
                if weaponName == "shotGun":
                    #tempX = 33
                    #tempY = 23
                    pass
               # if weaponName == "snipe":
                    #tempX += 10
                    #tempY += -15
              #      pass
        
            elif self.direction == "up":                               # left and up
                tempProjAngle = 270
                tempX = 8
                tempY = -2
                
                if weaponName == "shotGun":
                    tempY -= 15
                    tempX -= 3
                        


            projectileTemp = item.Projectile(self._character.getCurrentWeapon().getProjectileImage(), 
                                          self._character.rect,"randomShit", None,
                                          9, tempProjAngle, tempX, tempY, weaponPower)
            
            
            
            """            
            if self.direction == "up":
                tempProjAngle = 270
                tempX = 8
                tempY = -2
            elif self.direction == "down":
                if self._character.getDirection() == "right":
                    tempProjAngle = 45
                    tempY = 35
                    
                    if weaponName == "shotGun":
                        # down and right
                
                        pass
                                            
                    tempProjAngle = 135
                    # down and left
                    if weaponName == "shotGun":
                        tempX -= 33
                        tempY += 23
                        
                if weaponName == "snipe":
                    tempX += 10
                    tempY += -15
            else:
                if (self._character.getDirection() == "right"):
                    tempProjAngle = 0
                else:
                    tempProjAngle = 180  
                    tempX += -30
                                
                    
            projectileTemp = item.Projectile(self._character.getCurrentWeapon().getProjectileImage(), 
                                          self._character.rect,"randomShit", None,
                                          9, tempProjAngle, tempX, tempY, weaponPower)
            """
            angleList = []
            #angleList.append(324)
            #angleList.append(333)
            #angleList.append(342)
            angleList.append(351)
            #angleList.append(0)
            angleList.append(9)
            angleList.append(18)
            #angleList.append(27)
            #angleList.append(36)
            #angleList.append(45)
            
            

            if weaponName == "machine":
                self._character.machinegun.play()
                for i in range(0, 5, 1):
                    projectileTemp = item.Projectile(self._character.getCurrentWeapon().getProjectileImage(), 
                                          self._character.rect,"randomShit", None,
                                          9, tempProjAngle, tempX, tempY, weaponPower)
                    self._character.getCurrentWeapon().addProjectile(projectileTemp)
            elif weaponName == "shotGun":
                self._character.shotgun.play()
                for angle in angleList:
                    projectileTemp = item.Projectile(self._character.getCurrentWeapon().getProjectileImage(), 
                                          self._character.rect,"shotGunShit", None,
                                          9, angle + tempProjAngle, tempX, tempY, weaponPower)
                    self._character.getCurrentWeapon().addProjectile(projectileTemp)
            elif weaponName == "bazooka":
                self._character.bazooka.play()
                projectileTemp = item.Projectile(self._character.getCurrentWeapon().getProjectileImage(), 
                                          self._character.rect,"missile", None,
                                          9, tempProjAngle, tempX, tempY, weaponPower)
                self._character.getCurrentWeapon().addProjectile(projectileTemp)
            elif weaponName == "handGun":
                self._character.handgun.play()
                self._character.getCurrentWeapon().addProjectile(projectileTemp)
            else:
                self._character.sniper.play()
                self._character.getCurrentWeapon().addProjectile(projectileTemp)
                    

        
        # Testing for the powerUp safetyNet

# Working version of the saftyNet        
#        if self._counter == 1:
#            for i in range(0, 10, 1):
#                self._character.getCurrentPowerup().addPowerup(tempProjectile)
    
        """
        if self._frameNum == len(self.leftFrames) - 3: and \
        self._counter == 0:
            self.hurtSound.play()
        if self._frameNum >= len(self.leftFrames) - 3:
            self._character.attacking = True
        else:
            self._character.attacking = False
        """    
    
    def __str__(self):
        return "AttackingState"
    
class DeadState(State):
    def __init__(self, character, rightFrames, leftFrames):
        super(DeadState,self).__init__(character, rightFrames, leftFrames)
    
    def act(self):
        """
        Take away a character life. Set x and y velocity to zero
        """
        if self._character.getLives() > 1:
            self._character.setLives(self._character.getLives() - 1)
        else:
            pass
        self._character.velocity.x = 0
        self._character.velocity.y = 0
        
    def __str__(self):
        return "DeadState"
    
class TalkingState(State):
    def __init__(self, character, rightFrames, leftFrames):
        super(TalkingState,self).__init__(character, rightFrames, leftFrames)
    
    def act(self):
        """
        Will set the x and y velocity values to zero. Initiate dialog string
        from dialogFile.txt
        """
        pass
    
    def __str__(self):
        return "TalkingState"
    
class PowerupState(State):
    def __init__(self, character, rightFrames, leftFrames):
        super(PowerupState,self).__init__(character, rightFrames, leftFrames)
    
    def act(self):
        """
        Apply effects of a powerup to the character
        """
            
        if self._counter == 0 and self._frameNum == 1:
            tempProjectile = item.ProjectilePowerup(self._character.getSafetyNetImage(), self._character.rect, "safetyNet", None, 2)
            tempProjectile2 = item.ProjectilePowerup(self._character.getSafetyNetImage(), self._character.rect, "safetyNet", None, 2)
        
        self._character.getCurrentPowerup().addPowerup(tempProjectile)
        self._character.getCurrentPowerup().addPowerup(tempProjectile2)
        
        
        pass
    
    def __str__(self):
        return "PowerupState"

        
