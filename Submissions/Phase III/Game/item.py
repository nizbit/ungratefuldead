"""
Contents:
    Item
    Weapon
    Projectile
    Powerups
    BoostHP
    Invincibility
    InstaKill
"""
import math

class Item(object):
    def __init__(self, image, rect, name, sound):
        '''
        ** set items image              ==> pygame.image
        ** set items on-screen position ==> pygame.Rect
        ** set items name               ==> string
        ** set items sound              ==> pygame.mixer.Sound
        '''
        self._image = image
        self._rect = image.get_rect()
        self._rect.topleft = rect.topleft
        self._name = name
        self._sound = sound
    
    def getImage(self):
        return self._image
    
    def getRect(self):
        return self._rect
    
    def setName(self, name):
        self._name = name
    
    def getName(self):
        return self._name
    
    def playSound(self):
        _sound.play()
        
    '''virtual method to be overridden by child classes'''
    def update(self):
        pass
    
    '''argument ==> pygame.surface'''
    def render(self, surface):
        surface.blit(self._image, self._rect)
        
    
class Weapon(Item):
    def __init__(self, image, rect, name, sound, projectile = None, projectileImage = None, offSetx = None, offSety = None):
        '''
        ** call base class constructor
        ** set weapon items projectile ==> Projectile
        ** (a weapon only has a corresponding Projectile)
        '''
        
        super(Weapon, self).__init__(image, rect, name, sound)
        self._projectileList = []
        self._projectile = projectile

        if projectile != None:
            self._hasProjectileFlag = True
        else:
            self._hasProjectileFlag = False
        if offSetx == None:
            self._offSet_x = 0
        else:
            self._offSet_x = offSetx            
        if offSety == None:
            self._offSet_y = 0
        else:
            self._offSet_y = offSety
            
            
        self._projectileImage = projectileImage
    
    def getOffsetX(self):
        return self._offSet_x
    def getOffsetY(self):
        return self._offSet_y
    
    def getProjectileImage(self):
        return self._projectileImage
             
    def hasProjectile(self):
        return self._hasProjectileFlag
        
    def getProjectile(self):
        return self._projectile
    
    def setProjectile(self, projectile):
        self._projectile = projectile
        
    def addProjectile(self, projectile):
        self._projectileList.append(projectile)
        
    def removeProjectile(self, projectile):
        self._projectileList.remove(projectile)
        
    def getProjectileList(self):
        return self._projectileList

class Projectile(Item):
    def __init__(self, image, rect, name, sound, velocity, angle=None, offSetx = None, offSety = None, power=0, range=0):
        '''
        ** call base class constructor
        ** set projectile items velocity ==> Vector2D
        ** set projectile items power    ==> int
        ** set projectile items range    ==> int
        Note: Angle::
                270
            225     315
        180             0
            135     45
                90    
        '''
        super(Projectile, self).__init__(image, rect, name, sound)
        self._velocity = velocity
        self._power = power
        self._range = range
       
        self._offSetx = 30
        self._offSety = 11
        if offSetx == None:
            offSetx = 0
        if offSety == None:
            offSety = 0
        
        self._rect = self._rect.move(offSetx, offSety)

        if angle == None:
            self._angle = 0
        else:
            self._angle = angle 
            
    def getVelocity(self):
        return self._velocity
    
    def setVelocity(self, velocity):
        self._velocity = velocity
        
    def update(self, updateAngle = None):
        '''
        ** offset the projectile items rect by the current velocity
        '''
        if updateAngle != None:
            self._angle = updateAngle
        
        xPos = math.cos(math.radians(self._angle)) * self._velocity   
        yPos = math.sin(math.radians(self._angle)) * self._velocity
        self._rect = self._rect.move(xPos, yPos)


class ProjectilePowerup(Item):
    def __init__(self, image, rect, name, sound, velocity, jcount, power=0, range=0):
        '''
        ** call base class constructor
        ** set projectile items velocity ==> Vector2D
        ** set projectile items power    ==> int
        ** set projectile items range    ==> int
        Note: Angle::
                270
            225     315
        180             0
            135     45
                90    
        '''
        super(ProjectilePowerup, self).__init__(image, rect, name, sound)
        self._velocity = velocity
        self._power = power
        self._range = range
        self._jCounter = jcount
        #self._angle = math.radians(angle)
        
        self._offSetx = 33
        self._offSety = -13
        self._rect.move_ip(self._offSetx, self._offSety)
        (self._previousX, self._previousY) = rect.center
        self._firstRun = True
            
    def getVelocity(self):
        return self._velocity
    
    def setVelocity(self, velocity):
        self._velocity = velocity
        
    def update(self, rect):
        '''
        ** offset the projectile items rect by the current velocity
        '''
        #if self._firstRun:
        #    self._firstRun = False
        #else:
        #if self._jCounter >= 0:
        #    self._jCounter = 0
        self._jCounter += 10
        self._angle = math.radians(self._jCounter)
            
        #print self._jCounter
        (xT, yT) = rect.center

        xT += self._offSety
        yT += self._offSety
        xPos = math.cos(self._angle) * 10  
        yPos = math.sin(self._angle) * 10 

        xTemp = xT - self._previousX 
        yTemp =  yT - self._previousY
        
        xPos = math.trunc(xPos)
        yPos = math.trunc(yPos)
        
        self._rect.move_ip(xPos + xTemp, yPos + yTemp)
        
        (self._previousX, self._previousY) = rect.center
        self._previousX += self._offSety
        self._previousY += self._offSety
        
        
        

class SafetyNet(Item):
    def __init__(self, image, rect, name, sound):
       super(SafetyNet, self).__init__(image, rect, name, sound)
       #safetyNetImage = pygame.image.load("/Images/weaponPic/blackBullet.png").convert()
        
        
       #     def __init__(self, image, rect, name, sound, velocity, angle=None, power=0, range=0):
    #  safetyNetProjectile = item.Projectile(image, rect, "safetyNetProj", None, 3,  
        
     #  projectileTemp = item.Projectile(self._character.getCurrentWeapon().getProjectileImage(), 
      #                                    self._character.rect,"randomShit", None,
      #                                    9, projectileAngle)
        
        
        
    def update(self):
        pass
    
        
'''**base class for different types of powerups**'''
class Powerups(Item):
    def __init__(self, image, rect, name, sound):
        '''
        ** call base class constructor
        '''
        super(Powerups, self).__init__(image, rect, name, sound)
        
        self._powerUpList = []
        
    def addPowerup(self, thing):
        self._powerUpList.append(thing)
    def removePowerup(self, thing):
        self._powerUpList.remove(thing)
    def getPowerupList(self):
        return self._powerUpList
    

class BoostHP(Powerups):
    def __init__(self, image, rect, name, sound, amount=0):
        '''
        ** call parent class constructor
        ** set BoostHP Powerups' amount
        '''
        super(BoostHP, self).__init__(image, rect, name, sound)
        self._amount = amount
    
    def getAmmount(self):
        return self._amount
    
    def setAmmount(self, amount):
        self._amount = amount
    
class Invincibility(Powerups):
    def __init__(self, image, rect, name, sound, effectTime=0):
        '''
        ** call parent class constructor
        ** set Invincibility's Powerups' effect time 
        '''
        super(Invincibility, self).__init__(image, rect, name, sound)
        self._effectTime = effectTime
    
    def getEffectTime(self):
        return self._effectTime
    
    def setEffectTime(self, effectTime):
        self._effectTime = effectTime

class InstaKill(Powerups):
    def __init__(self, image, rect, name, sound, amount=0):
        '''
        ** call parent class constructor
        ** set InstaKill Powerups' amount
        '''
        super(InstaKill, self).__init__(image, rect, name, sound)
        self._amount = amount

    def killCharacter(self, character):
        '''
        ** take amount of HP away from the character
        '''
        if character.getHP() >= amount:
            character.setHP(character.getHP() - amount)
        else:
            character.setHP(0)