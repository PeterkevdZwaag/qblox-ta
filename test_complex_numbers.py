from complex_numbers import Complex
import pytest
import math

@pytest.mark.parametrize("re, im", [
    ("not a number", 2),
    (1, "not a number"),
    (None, 2),
    (1, [1, 2]),
])
def test_init_rejects_non_numeric_input(re, im):
    with pytest.raises(TypeError):
        Complex(re, im)

@pytest.mark.parametrize("re, im", [
    (1, 2),          # two ints
    (1.5, 2.5),      # two floats
    (1, 2.5),        # mixed int/float
    (-1, -2),        # negative numbers
    (0, 0),          # zero
])
def test_init_accepts_valid_numeric_input(re, im):
    Complex(re, im)  # should not raise

@pytest.mark.parametrize("r, theta, expected_re, expected_im", [
    (1, 0, 1, 0),             # 1
    (2, math.pi/2, 0, 2),     # 2i
    (5, math.atan2(-4, -3), -3, -4), # -3 -4i
    (2, math.atan2(-1, 1), 2**0.5, -2**0.5),   # 2**0.5 -2**0.5i
    (0, 0, 0, 0),             # 0
])
def test_from_polar(r, theta, expected_re, expected_im):
    c = Complex.from_polar(r, theta)
    assert math.isclose(c.re, expected_re, abs_tol=1e-9)
    assert math.isclose(c.im, expected_im, abs_tol=1e-9)

@pytest.mark.parametrize("re, im, expected_str", [
    (1, 0, "1"),
    (0, 1, "1i"),
    (0, 0, "0"),
])
def test_str(re, im, expected_str):
    c = Complex(re, im)
    assert str(c) == expected_str

@pytest.mark.parametrize("a, b, expected_re, expected_im", [
    (Complex(1, 2), Complex(3,4), 4, 6),
    (Complex(1, 2), Complex(-1, -2), 0, 0),
    (Complex(0.5, -0.5), 2, 2.5, -0.5),
    (-3, Complex(0, 4.1),-3, 4.1),
])
def test_add(a, b, expected_re, expected_im):
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

@pytest.mark.parametrize("a, b, expected_re, expected_im", [
    (Complex(3, 4), Complex(1, 2), 2, 2),
    (Complex(-2, -1), 5, -7, -1),
    (4.4, Complex(4.4, 3), 0, -3)
])
def test_sub(a, b, expected_re, expected_im):
    c = a - b
    d = b - a
    assert c.re == expected_re
    assert c.im == expected_im
    assert c == -d







