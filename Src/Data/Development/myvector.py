import math

class Vector(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)
    
    @classmethod
    def makeVect(cls, P1, P2): 
        return cls(P2[0] - P1[0], P2[1] - P1[1])
    
    def getLength(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normal(self):
        return (self.x / self.getLength(), self.y / self.getLength())

def main():
    A = (10, 30)
    B = (20, 40)
    Vector.AB = Vector.makeVect(A, B)
    print Vector.AB
    print Vector.getLength(Vector.AB)
    print Vector.normal(Vector.AB)   
    
if __name__ == "__main__":
    main()