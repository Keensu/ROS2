import math

from museum_guide.distance_monitor import calculate_distance


def test_zero_distance():
    assert calculate_distance(0.0, 0.0, 0.0, 0.0) == 0.0


def test_distance_3_4_5():
    assert calculate_distance(0.0, 0.0, 3.0, 4.0) == 5.0


def test_distance_negative_coords():
    assert calculate_distance(-1.0, -1.0, 2.0, 3.0) == 5.0


def test_distance_symmetric():
    d1 = calculate_distance(1.0, 2.0, 4.0, 6.0)
    d2 = calculate_distance(4.0, 6.0, 1.0, 2.0)
    assert d1 == d2


def test_distance_float():
    d = calculate_distance(0.0, 0.0, 1.0, 1.0)
    assert math.isclose(d, math.sqrt(2), rel_tol=1e-9)
