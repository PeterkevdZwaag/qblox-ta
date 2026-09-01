import math
from numbers import Real

class Complex:
    
    def __init__(self, re: Real, im: Real):

        if not isinstance(re, Real) or not isinstance(im, Real):
            raise TypeError(f"re and im must be real numbers, got {type(re).__name__} and {type(im).__name__}")
        self._re = re
        self._im = im

    @classmethod
    def from_polar(cls, r: Real, theta: Real) -> "Complex":
        return cls(r * math.cos(theta), r * math.sin(theta))

    @property
    def re(self) -> Real:
        return self._re

    @property
    def im(self) -> Real:
        return self._im

    @property
    def r(self) -> float:
        return math.hypot(self._re, self._im)

    @property
    def theta(self) -> float:
        return math.atan2(self._im, self._re)

    def __str__(self):
        if self.im == 0:
            return f"{self.re}"
        elif self.re == 0:
            return f"{self.im}i"
        return f"{self.re} + {self.im}i"
    
    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.re + other.re, self.im + other.im)
        elif isinstance(other, Real):
            return Complex(self.re+other, self.im)
        else:
            raise TypeError(f"Cannot add Complex and {type(other).__name__}")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.re - other.re, self.im - other.im)
        elif isinstance(other, Real):
            return Complex(self.re - other, self.im)
        else:
            raise TypeError(f"Cannot substract {type(other).__name__} from Complex")

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __abs__(self) -> float:
        return self.r

    def __neg__(self):
        return Complex(-self.re, -self.im)

    def __mul__(self,other):
        return Complex(self.re*other.re - self.im*other.im, self.re*other.im + self.im*other.re)

    def __truediv__(self, other):
        denom = other.re**2 + other.im**2
        re = (self.re*other.re +self.im*other.im)/denom
        im = (self.im*other.re-self.re*other.im)/denom
        return Complex(re, im)
    
    def __eq__(self, other):
        if isinstance(other, Complex):
            return math.isclose(self.re, other.re) and math.isclose(self.im, other.im)
        elif isinstance(other, Real):
            return self.im == 0 and math.isclose(self.re, other)
        else:
            return NotImplemented

    
    


a = Complex(3, 4)
b = Complex(3,0)
print(a)
print(b)
print(a/b)