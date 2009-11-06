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

class Item(Object):
    def __init__(self):
        pass

class Weapon(Item):
    def __init__(self):
        pass

class Projectile(Item):
    def __init__(self):
        pass

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
