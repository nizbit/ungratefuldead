import math

class vector():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vector = 0
    
    def makeVector(self, u, v):
        vector = (v[0] - u[0], v[1] - u[1])
        return self.vector
    
    def isEqual(self, u):
        if self.x == u[0] and self.y == u[1]:
            return True
        else:
            return False

