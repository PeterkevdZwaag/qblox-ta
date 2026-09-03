import math

import pytest

from complex_numbers import Complex


@pytest.mark.parametrize(
    "re, im",
    [
        ("not a number", 2),
        (1, "not a number"),
        (None, 2),
        (1, [1, 2]),
    ],
)
def test_init_invalid_input(re, im):
    with pytest.raises(TypeError):
        Complex(re, im)


@pytest.mark.parametrize(
    "re, im",
    [
        (1, 2),  # two ints
        (1.5, 2.5),  # two floats
        (1, 2.5),  # mixed int/float
        (-1, -2),  # negative numbers
        (0, 0),  # zero
    ],
)
def test_init(re, im):
    c = Complex(re, im)
    assert c.re == re
    assert c.im == im
    assert c.r == math.hypot(re, im)
    assert c.theta == math.atan2(im, re)


@pytest.mark.parametrize(
    "r, theta, expected_re, expected_im",
    [
        (1, 0, 1, 0),  # 1
        (2, math.pi / 2, 0, 2),  # 2i
        (3, math.pi, -3, 0),  # -3
        (4, 3 * math.pi / 2, 0, -4),  # -4i
        (5, math.atan2(-4, -3), -3, -4),  # -3 -4i
        (2, math.atan2(-1, 1), 2**0.5, -(2**0.5)),  # 2**0.5 -2**0.5i
        (0, 0, 0, 0),  # 0
    ],
)
def test_from_polar(r, theta, expected_re, expected_im):
    c = Complex.from_polar(r, theta)
    assert math.isclose(c.re, expected_re, abs_tol=1e-9)
    assert math.isclose(c.im, expected_im, abs_tol=1e-9)


@pytest.mark.parametrize(
    "r, theta",
    [
        ("not a number", 2),
        (1, "not a number"),
        (None, 2),
        (1, [1, 2]),
    ],
)
def test_from_polar_invalid(r, theta):
    with pytest.raises(TypeError):
        Complex.from_polar(r, theta)


@pytest.mark.parametrize(
    "re, im, expected_str",
    [
        (1, 0, "1"),
        (0, 1, "1i"),
        (0, 0, "0"),
        (1, 1, "1 + 1i"),
    ],
)
def test_str(re, im, expected_str):
    c = Complex(re, im)
    assert str(c) == expected_str


def test_repr():
    c = Complex(1, 2)
    assert repr(c) == "Complex(1, 2)"


@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        (Complex(1, 2), Complex(1, 2), True),
        (Complex(1, 2), Complex(2, 1), False),
        (Complex(1, 0), 1, True),
        (Complex(0, 1), 1, False),
        (0.5, Complex(0.5, 0), True),
        (5, Complex(5, 5), False),
        (Complex(0, 0), 0, True),
        (Complex(0.1 + 0.2, 0), Complex(0.3, 0), False),
        (Complex.from_polar(1, math.pi), -1, False),
    ],
)
def test_eq(a, b, expected_result):
    result = a == b
    assert result == expected_result


def test_eq_invalid():
    a = Complex(1, 1)
    b = []
    c = None
    with pytest.raises(TypeError):
        a == b
    with pytest.raises(TypeError):
        c == a


@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        (Complex(1, 2), Complex(1, 2), True),
        (Complex(1, 2), Complex(2, 1), False),
        (Complex(1, 0), 1, True),
        (Complex(0, 1), 1, False),
        (Complex(0, 0), 0, True),
        (Complex(0.1 + 0.2, 0), Complex(0.3, 0), True),
        (Complex.from_polar(1, math.pi), -1, True),
    ],
)
def test_isclose(a, b, expected_result):
    result = a.isclose(b)
    assert result == expected_result


def test_isclose_invalid():
    a = Complex(1, 1)
    b = []
    c = None
    with pytest.raises(TypeError):
        a.isclose(b)
    with pytest.raises(TypeError):
        a.isclose(c)


@pytest.mark.parametrize(
    "a, b, expected_re, expected_im",
    [
        (Complex(1, 2), Complex(3, 4), 4, 6),
        (Complex(1, 2), Complex(-1, -2), 0, 0),
        (Complex(0.5, -0.5), 2, 2.5, -0.5),
        (-3, Complex(0, 4.1), -3, 4.1),
    ],
)
def test_add_and_radd(a, b, expected_re, expected_im):
    c = a + b
    d = b + a
    assert c.re == expected_re
    assert c.im == expected_im
    assert c == d


def test_add_invalid():
    a = Complex(1, 1)
    b = "string"
    with pytest.raises(TypeError):
        a + b
    with pytest.raises(TypeError):
        b + a


@pytest.mark.parametrize(
    "a, b, expected_re, expected_im",
    [
        (Complex(3, 4), Complex(1, 2), 2, 2),
        (Complex(-2, -1), 5, -7, -1),
        (4.4, Complex(4.4, 3), 0, -3),
    ],
)
def test_sub_and_rsub(a, b, expected_re, expected_im):
    c = a - b
    d = b - a
    assert c.re == expected_re
    assert c.im == expected_im
    assert c == -d


def test_sub_invalid():
    a = Complex(1, 1)
    b = "string"
    with pytest.raises(TypeError):
        a - b
    with pytest.raises(TypeError):
        b - a


@pytest.mark.parametrize(
    "a, b, expected_re, expected_im",
    [
        (Complex(1, 2), Complex(3, 4), -5, 10),
        (Complex(1.5, 0.3), -2, -3, -0.6),
        (0.1, Complex(5, 2), 0.5, 0.2),
        (Complex(4, 3), 0, 0, 0),
    ],
)
def test_mul_and_rmul(a, b, expected_re, expected_im):
    c = a * b
    d = b * a
    assert c.re == expected_re
    assert c.im == expected_im
    assert c == d


def test_mul_invalid():
    a = Complex(1, 1)
    b = "string"
    with pytest.raises(TypeError):
        a * b
    with pytest.raises(TypeError):
        b * a


@pytest.mark.parametrize(
    "a, e, expected_re, expected_im",
    [
        (Complex(4, -3), 0, 1, 0),
        (Complex(4, -3), 1, 4, -3),
        (Complex(1, 2), 2, -3, 4),
        (Complex(-3, 4), 0.5, 1, 2),
        (Complex(2, -1), -1, 0.4, 0.2),
        (Complex(0, 0), 0.1, 0, 0),
    ],
)
def test_pow(a, e, expected_re, expected_im):
    c = a**e
    assert math.isclose(c.re, expected_re, abs_tol=1e-9)
    assert math.isclose(c.im, expected_im, abs_tol=1e-9)
    assert c.isclose(Complex(expected_re, expected_im))


def test_pow_invalid():
    a = Complex(1, 1)
    e = "string"
    with pytest.raises(TypeError):
        a**e
    with pytest.raises(TypeError):
        a**a


@pytest.mark.parametrize(
    "a, b, expected_re, expected_im",
    [
        (Complex(3, 6), 3, 1, 2),
        (Complex(2, 2), Complex(1, 1), 2, 0),
    ],
)
def test_truediv_and_rtruediv(a, b, expected_re, expected_im):
    c = a / b
    d = b / a

    assert c.re == expected_re
    assert c.im == expected_im
    assert abs(c * d) == 1
    assert (c * d) == 1


@pytest.mark.parametrize(
    "a, b",
    [
        (Complex(0, 0), Complex(5, -2)),
        (Complex(0, 0), 3.14),
        (0, Complex(1, 0)),
        (0, Complex(5, 6)),
    ],
)
def test_truediv_and_rtruediv0(a, b):
    c = a / b
    assert c.re == 0
    assert c.im == 0
    assert c == 0


def test_truediv_and_rtruediv_invalid():
    a = Complex(1, 1)
    b = "string"
    with pytest.raises(TypeError):
        a / b
    with pytest.raises(TypeError):
        b / a


@pytest.mark.parametrize(
    "a, b",
    [
        (Complex(3, 4), 0),  # Complex(not 0) / 0            -> __truediv__
        (Complex(3, 4), Complex(0, 0)),  # Complex(not 0) / Complex(0,0) -> __truediv__
        (5, Complex(0, 0)),  # not 0 / Complex(0,0)          -> __rtruediv__
        (0, Complex(0, 0)),  # 0 / Complex(0,0)              -> __rtruediv__
        (Complex(0, 0), Complex(0, 0)),  # Complex(0,0) / Complex(0,0)   -> __truediv__
    ],
)
def test_truediv_and_rtruediv_by_zero_raises(a, b):
    with pytest.raises(ZeroDivisionError):
        a / b


@pytest.mark.parametrize(
    "c, expected_result",
    [
        (Complex(1, 2), Complex(1, -2)),
        (Complex(-1, -2), Complex(-1, 2)),
        (Complex(3, 0), Complex(3, 0)),
    ],
)
def test_conjugate(c, expected_result):
    result = c.conjugate()
    assert result == expected_result
    assert c.im + result.im == 0
