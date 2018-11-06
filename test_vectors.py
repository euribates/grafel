#!/usr/bin/env python3


import math

import pytest
from vectors import Vector, get_random_unitary_vector


def test_create():
    v = Vector(3, 4)
    assert v.x == 3.0
    assert v.width == 3.0
    assert v.y == 4.0
    assert v.height == 4.0


def test_create_unit_vector_right():
    right = Vector(1, 0)
    assert right.mod == 1.0
    assert math.isclose(right.theta, 0.0)


def test_create_unit_vector_left():
    left = Vector(-1, 0)
    assert left.mod == 1.0
    assert math.isclose(left.theta, math.pi)


def test_create_unit_vector_up():
    up = Vector(0, 1)
    assert up.mod == 1.0
    assert math.isclose(up.theta, math.pi / 2.0)


def test_create_unit_vector_down():
    down = Vector(0, -1)
    assert down.mod == 1.0
    assert math.isclose(down.theta, -math.pi / 2.0)


def test_create_random_unit_vector():
    for i in range(1000):
        v = get_random_unitary_vector()
        assert -1.0 < v.x < 1.0
        assert -1.0 < v.y < 1.0
        assert math.isclose(v.mod, 1.0)


def test_modulo():
    v = Vector(3, 4)
    assert v.mod == 5.0
    v = Vector(30, 0)
    assert v.mod == 30.0
    v = Vector(0, 30)
    assert v.mod == 30.0


def test_modificar_modulo_no_afecta_al_angulo():
    v = Vector(3, 4)
    theta = v.theta
    assert math.isclose(v.mod, 5.0)
    v.mod *= 12
    assert math.isclose(v.mod, 60.0)
    assert math.isclose(v.x, 36.0)
    assert math.isclose(v.y, 48.0)
    assert math.isclose(v.theta, theta)


def test_decremet_module_does_not_modify_angle():
    v = Vector(36, 48)
    theta = v.theta
    for i in range(80):
        v.mod *= 0.95
        assert math.isclose(v.theta, theta)


def test_get_theta():
    v = Vector(30, 0)
    assert math.isclose(v.theta, 0.0)
    v = Vector(30, 30)
    assert math.isclose(v.theta, math.pi / 4.0)
    v = Vector(-30, 0)
    assert math.isclose(v.theta, math.pi)


def test_set_theta():
    v = Vector(3, 4)
    v.theta = 0.0
    assert math.isclose(v.x, 5.0)
    assert math.isclose(v.y, 0.0)
    v.theta = math.pi / 2.0
    assert math.isclose(v.x, 0.0)
    assert math.isclose(v.y, 5.0)


def test_add(): 
    v1 = Vector(3, 4)
    v2 = Vector(5, -2)
    v3 = v1 + v2
    assert math.isclose(v3.x, 8.0)
    assert math.isclose(v3.y, 2.0)


def test_mul():
    v = Vector(3, 4) * 2
    assert math.isclose(v.x, 6.0)
    assert math.isclose(v.y, 8.0)


def test_div():
    v = Vector(6, 8) / 2
    assert math.isclose(v.x, 3.0)
    assert math.isclose(v.y, 4.0)


def test_equal():
    v1 = Vector(3, 4)
    v2 = Vector(3, 4)
    assert v1 == v2
    assert v1 == (3, 4)
    assert v2 == (3, 4)


def test_tuple_asigment():
    v = Vector(3, 4)
    (a, b) = v
    assert a == v.x
    assert b == v.y


def test_access_by_index():
    v = Vector(3, 4)
    assert v[0] == 3.0
    assert v[1] == 4.0


if __name__ == '__main__':
    unittest.main()

