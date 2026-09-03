from __future__ import annotations

import math
from numbers import Real


class Complex:
    def __init__(self, re: Real, im: Real):
        if not isinstance(re, Real) or not isinstance(im, Real):
            raise TypeError(
                f"re and im must be real numbers, got {type(re).__name__} and {type(im).__name__}"
            )
        self._re = re
        self._im = im

    @classmethod
    def from_polar(cls, r: Real, theta: Real) -> Complex:
        if not isinstance(r, Real) or not isinstance(theta, Real):
            raise TypeError(
                f"r and theta must be real numbers, got {type(r).__name__} and {type(theta).__name__}"
            )
        return cls(r * math.cos(theta), r * math.sin(theta))

    @property
    def re(self) -> Real:
        """The real part of the complex number."""
        return self._re

    @property
    def im(self) -> Real:
        """The imaginary part of the complex number."""
        return self._im

    @property
    def r(self) -> float:
        """The magnitude of the complex number."""
        return math.hypot(self._re, self._im)

    @property
    def theta(self) -> float:
        """The angle, in radians, of the complex number."""
        return math.atan2(self._im, self._re)

    def __str__(self) -> str:
        """Return a human-readable string, e.g. '3 + 4i'."""
        if self.im == 0:
            return f"{self.re}"
        if self.re == 0:
            return f"{self.im}i"
        if self.im < 0:
            return f"{self.re} - {-self.im}i"
        return f"{self.re} + {self.im}i"

    def __repr__(self) -> str:
        """Return printable representation for debugging."""
        return f"Complex({self.re!r}, {self.im!r})"

    def __add__(self, other: Real | Complex) -> Complex:
        """Add a Complex or real number to this Complex number."""
        if isinstance(other, Complex):
            return Complex(self.re + other.re, self.im + other.im)
        if isinstance(other, Real):
            return Complex(self.re + other, self.im)
        raise TypeError(f"Cannot add Complex and {type(other).__name__}")

    def __radd__(self, other: Real | Complex) -> Complex:
        """Add this Complex number to a real or Complex number."""
        return self.__add__(other)

    def __sub__(self, other: Real | Complex) -> Complex:
        """Substract a Complex or real number from this Complex number."""
        if isinstance(other, Complex):
            return Complex(self.re - other.re, self.im - other.im)
        if isinstance(other, Real):
            return Complex(self.re - other, self.im)
        raise TypeError(f"Cannot substract {type(other).__name__} from Complex")

    def __rsub__(self, other: Real | Complex) -> Complex:
        """Substract this Complex number from a real or Complex number."""
        return -self.__sub__(other)

    def __abs__(self) -> float:
        """Return the absolute value of the Complex number."""
        return self.r

    def __neg__(self) -> Complex:
        """Return the negation of the Complex number."""
        return Complex(-self.re, -self.im)

    def __mul__(self, other: Real | Complex) -> Complex:
        """Multiply this Complex number by a Complex or real number."""
        if isinstance(other, Complex):
            return Complex(
                self.re * other.re - self.im * other.im,
                self.re * other.im + self.im * other.re,
            )
        if isinstance(other, Real):
            return Complex(other * self.re, other * self.im)
        raise TypeError(f"Cannot multiply Complex with {type(other).__name__}")

    def __rmul__(self, other: Real | Complex) -> Complex:
        """Multiply a Complex or real number by this Complex number."""
        return self.__mul__(other)

    def __pow__(self, exp: Real) -> Complex:
        """Raise this Complex number to a real power."""
        # for exp = 0, 1, 2, etc., use __mul__ to calculate exact result
        if isinstance(exp, int) and exp >= 0:
            result = Complex(1, 0)
            for _ in range(exp):  # use __mul__ to calculate exact result
                result = result * self
            return result
        if isinstance(exp, Real):
            new_r = self.r**exp
            new_theta = self.theta * exp
            return Complex.from_polar(new_r, new_theta)
        raise TypeError(f"Unsupported exponent type: {type(exp).__name__}")

    def __truediv__(self, other: Real | Complex) -> Complex:
        """Divide this Complex number by a real or Complex number."""
        try:
            if abs(other) == 0:
                raise ZeroDivisionError("Cannot divide Complex by 0")
        except TypeError:
            pass # TypeErrors caught below
        if isinstance(other, Complex):
            denom = other.re**2 + other.im**2
            re = (self.re * other.re + self.im * other.im) / denom
            im = (self.im * other.re - self.re * other.im) / denom
            return Complex(re, im)
        if isinstance(other, Real):
            return Complex(self.re / other, self.im / other)
        raise TypeError(f"Cannot do division with Complex and {type(other).__name__}")

    def __rtruediv__(self, other: Real | Complex) -> Complex:
        """Divide a real or Complex number by this Complex number."""
        return Complex(other, 0) / self

    def __eq__(self, other: Real | Complex) -> bool:
        """Check exact equality with another Complex or real number."""
        if isinstance(other, Complex):
            return self.re == other.re and self.im == other.im
        if isinstance(other, Real):
            return self.re == other and self.im == 0
        raise TypeError(f"Cannot compare Complex and {type(other).__name__}")

    def isclose(self, other: Real | Complex, abs_tol=1e-9) -> bool:
        """Check approximate equality with another Complex or real number."""
        if isinstance(other, Complex):
            return math.isclose(self.re, other.re, abs_tol=abs_tol) and math.isclose(
                self.im, other.im, abs_tol=abs_tol
            )
        if isinstance(other, Real):
            return math.isclose(self.im, 0, abs_tol=abs_tol) and math.isclose(
                self.re, other, abs_tol=abs_tol
            )

        raise TypeError(f"Cannot compare Complex and {type(other).__name__}")

    def conjugate(self) -> Complex:
        """Return the conjugate of the Complex number."""
        return Complex(self.re, -self.im)
    
    def get_cartesian(self) -> tuple[Real, Real]:
        """Return (re, im) as a tuple."""
        return self.re, self.im
    
    def get_polar(self) -> tuple[Real, Real]:
        """Return (r, theta) as a tuple."""
        return self.r, self.theta


# TODO .ruff.toml file
# TODO: Ruff format, Ruff linter
# TODO: packaging: pyproject.toml
