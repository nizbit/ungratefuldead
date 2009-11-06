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

class Item(object):
    def __init__(self, image, rect, name, sound):
        '''
        ** set items image              ==> pygame.image
        ** set items on screen position ==> pygame.Rect
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
        
    def update(self):
        pass
    
    '''argument ==> pygame.surface'''
    def render(self, surface):
        surface.blit(self._image, self._rect)
        
    
class Weapon(Item):
    def __init__(self, image, rect, name, projectile):
        super(Projectile, self).__init__(image, rect, name, None)
        self._projectile = projectile

class Projectile(Item):
    def __init__(self, image, rect, name, sound, velocity, power, range):
        '''
        ** call base class constructor
        ** set projectile items velocity ==> Vector2D
        ** set projectile items power    ==> int
        ** set projectile items range    ==> int
        '''
        super(Projectile, self).__init__(image, rect, name, sound)
        self._velocity = velocity
        self._power = power
        self._range = range
        
    def getVelocity(self):
        return self._velocity
    
    def setVelocity(self, velocity):
        self._velocity = velocity
        
    def update(self):
        '''
        ** offset the projectile items rect by the current velocity
        '''
        self._rect = self._rect.move(self._velocity.get_x(), self._velocity.get_y())
        

class Powerups(Item):
    def __init__(self):
        pass

class BoostHP(Powerups):
    def __init__(self):
        pass
    
class Invincibility(Powerups):
    def __init__(self):
        pass

class InstaKill(Powerups):
    def __init__(self):
        pass
