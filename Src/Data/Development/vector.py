'''J. David B. ==> base vector class, has not been tested'''

class Vector(object):
    def __init__(self, x=0, y=0, z=0):
        self.componentX = x
        self.componentY = y
        self.componentZ = z
        self.vector = (componentX, componentY, componentZ)
    
    def __add__(self, v):
        return Vector(self.componentX + v.componentX,
                      self.componentY + v.componentY,
                      self.componentZ + v.componentZ)
    
    def __sub__(self, v):
        return Vector(self.componentX - v.componentX,
                      self.componentY - v.componentY,
                      self.componentZ - v.componentZ)
        
    '''DOT product ==> scalar quantity'''
    def __mul__(self, v):
        return (self.componentX * v.componentX) \
               + (self.componentY * v.componentY) \
               + (self.componentZ * v.componentZ)
    
    '''CROSS product ==> vector (we can fabricate an operator later if need be)'''
    def cross(self, v):
        i = self.componentX*((self.componentY*v.componentZ)-(self.componentZ*v.componentY))
        j = -(self.componentY*((self.componentX*v.componentZ)-(self.componentZ*v.componentX)))
        k = self.componentZ*((self.componentX*v.componentY)-(self.componentY*v.componentX))
        return Vector(i, j, k)