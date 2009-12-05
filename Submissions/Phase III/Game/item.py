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
        self._rect = rect
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
    def __init__(self, image, rect, name, sound, projectile = None, projectileImage = None):
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
            
            
        self._projectileImage = projectileImage
    
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
    def __init__(self, image, rect, name, sound, velocity, angle=None, power=0, range=0):
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
        
        

class SafetyNet(Item):
    def __init__(self, image, rect, name, sound):
        super(SafetyNet, self).__init__(image, rect, name, sound)
        
    def update(self):
        pass
    
        
'''**base class for different types of powerups**'''
class Powerups(Item):
    def __init__(self, image, rect, name, sound):
        '''
        ** call base class constructor
        '''
        super(Powerups, self).__init__(image, rect, name, sound)

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