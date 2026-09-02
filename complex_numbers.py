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
        if isinstance(other, Complex):
            return Complex(self.re*other.re - self.im*other.im, self.re*other.im + self.im*other.re)
        elif isinstance(other, Real):
            return Complex(other*self.re, other*self.im)
        else:
            raise TypeError(f"Cannot multiply Complex with {type(other).__name__}")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, exp) -> "Complex":
        if isinstance(exp, int) and exp >= 0:
            result = Complex(1, 0)
            for _ in range(exp):
                result = result * self
            return result
        elif isinstance(exp, Real):
            new_r = self.r ** exp
            new_theta = self.theta * exp
            return Complex.from_polar(new_r, new_theta)
        else:
            raise TypeError(f"Unsupported exponent type: {type(exponent).__name__}")

    def __truediv__(self, other):
        try:
            if abs(other) == 0:
                raise ZeroDivisionError(f"Cannot divide Complex by 0")
        except TypeError:
            pass
        if isinstance(other, Complex):
            denom = other.re**2 + other.im**2
            re = (self.re*other.re +self.im*other.im)/denom
            im = (self.im*other.re-self.re*other.im)/denom
            return Complex(re, im)
        elif isinstance(other, Real):
            return Complex(self.re/other, self.im/other)
        else:
            raise TypeError(f"Cannot do division with Complex and {type(other).__name__}")
        
    
    def __rtruediv__(self, other):
        return Complex(other, 0) / self

    def __eq__(self, other):
        if isinstance(other, Complex):
            return self.re == other.re and self.im == other.im
        elif isinstance(other, Real):
            return self.re == other and self.im == 0
        else:
            raise TypeError(f"Cannot compare Complex and {type(other).__name__}")

    def isclose(self, other, abs_tol=1e-9):
        if isinstance(other, Complex):
            return math.isclose(self.re, other.re, abs_tol=abs_tol) and math.isclose(self.im, other.im, abs_tol=abs_tol)
        elif isinstance(other, Real):
            return math.isclose(self.im, 0, abs_tol=abs_tol) and math.isclose(self.re, other, abs_tol=abs_tol)
        else:
            raise TypeError(f"Cannot compare Complex and {type(other).__name__}")

# TODO
# self.get_polar -> Tuple
# self.get_cartesian -> Tuple