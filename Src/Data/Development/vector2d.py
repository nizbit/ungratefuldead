"""
" * vector2D.py
" * Submitted as part of Phase III for EECS 448, Fall 2009
" *   Name Kernal Panic
" *   KUID 
" *
"""


class Vector2D(object):
    """
    " * Vector2D
    """
    def __init__(self, *values):
        """
        " * Class Constructor
        " *    data: A numeric two-tuple representing the vector.
        """
        self.__x = values[0]
        self.__y = values[1]
        
    def get_x(self):
        return self.__x
    
    def set_x(self, value):
        self.__x = value
        
    x = property(get_x, set_x)
        
    def get_y(self):
        return self.__y
    
    def set_y(self, value):
        self.__y = value
        
    y = property(get_y, set_y)
    
    def __repr__(self):
        """
        " * Vector2D String representation
        " *    @return: A string
        """
        return "Vector2D(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __eq__(self, other):
        """
        " * Vector2D Equality
        " *    @param other: A Vector2D object
        " *    @return: A boolean
        """
        return self.x == other.x and self.y == other.y
    
    def __mul__(self, scalar):
        """
        " * Vector2D Scalar Multiplication
        " *    @param scalar: A numeric scalar
        " *    @return: A Vector2D object
        """
        return Vector2D(self.x * scalar, self.y * scalar)
    
    __rmul__ = __mul__
    """ Right mult. is equal to left mult. when dealing with scalar values. """
        
    def __neg__(self):
        """
        " * Vector2D Negation
        " *    @return: A Vector2D object
        """
        return Vector2D(self.x * -1, self.y * -1)
    
    def __add__(self, other):
        """
        " * Vector2D Vector Addition (self + other)
        " *    @param other: A Vector2D object
        " *    @return: A Vector2D object
        """
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __radd__(self, other):
        """
        " * Vector2D Vector Addition (other + self)
        " *    @param other: A Vector2D object
        " *    @return: A Vector2D object
        """
        return Vector2D(self.x + other.x, self.y + other.y)
    
         
if __name__ == "__main__":
    """
    " * Unit Testing for Vector2D
    """
    import unittest
    import random
    
    
    class __VectorSpaceAxioms(unittest.TestCase):
        """
        " * Vector Space Axiom Testcase
        " *   The purpose of this test case is verify the eight defined axioms
        " *   of a vector space.
        """
        
        def test_commutativity(self):
            """ 
            " * Commutativity of Addition
            " *   Given: vectors u, v, w
            " *   u + v = v + u
            """
            
            u = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            v = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            w = u + v
            temp = v + u
            self.assertEqual(temp, w)
        
        def test_associativity(self):
            """ 
            " * Associativity of Addition
            " *   Given: vectors u, v, w
            " *   u + (v + w) = (u + v) + w
            """
            u = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            v = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            w = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            
            temp = u + (v + w)
            result = (u + v) + w
            self.assertEqual(result, temp)
        
        def test_identity(self):
            """ 
            " * Identity Element of Addition
            " *   Given: vectors v, 0; where 0 is the zero vector.
            " *   v + 0 = v
            """
            v = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            temp = v + Vector2D(0,0)
            self.assertEqual(v, temp)
        
        def test_additive_inverse(self):
            """ 
            " * Inverse Elements of Addition
            " *   Given: vectors v, w; where w is the additive inverse of v.
            " *   v + w = 0
            """
            v = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            w = -v
            result = v + w
            self.assertEqual(result, Vector2D(0,0))
        
        def test_distributivity(self):
            """ 
            " * Distributivity of Scalar Multiplication
            " *   Given: vectors v, w and scalar a
            " *   a(v + w) = av + aw
            """
            v = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            w = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            a = random.randint(-9999, 9999)
            lhs = a*(v + w)
            rhs = a * v + a * w
            self.assertEqual(lhs, rhs)
        
        def test_compatability_of_multiplication(self):
            """ 
            " * Compatability of Scalar and Field Multiplication
            " *   Given: vector v and scalars a, b
            " *   (ab)v = a(bv)
            """
            a = random.randint(-9999, 9999)
            b = random.randint(-9999, 9999)
            v = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            
            result1 = (a * b) * v
            result2 = a * (b * v)
            self.assertEqual(result1, result2)
        
        def test_identity_element(self):
            """ 
            " * Distributivity of Scalar Multiplication
            " *   Given: vectors v
            " *   1v = v
            """
            v = Vector2D(random.randint(-9999, 9999), random.randint(-9999, 9999))
            result = 1 * v
            self.assertEqual(v, result)
            
        
    unittest.main()