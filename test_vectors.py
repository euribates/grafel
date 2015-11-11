#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_vector.py

import math
import unittest

import vectors

from vectors import Vector

class Uso(unittest.TestCase):

    def test_creacion(self):
        v = Vector(3, 4)
        self.assertEqual(v.x, 3.0)
        self.assertEqual(v.width, 3.0)
        self.assertEqual(v.y, 4.0)
        self.assertEqual(v.height, 4.0)

    def test_get_random_unitary_value(self):
        for i in range(1000):
            v = vectors.get_random_unitary_vector()
            self.assertTrue(-1.0 < v.x < 1.0)
            self.assertTrue(-1.0 < v.y < 1.0)
            self.assertAlmostEqual(v.mod, 1.0)

    def test_creacion_vectores_unitarios(self):
        # Right
        right = Vector(1, 0)
        self.assertEqual(right.mod, 1.0)
        self.assertAlmostEqual(right.theta, 0.0)
        # Left
        left = Vector(-1, 0)
        self.assertEqual(left.mod, 1.0)
        self.assertAlmostEqual(left.theta, math.pi)
        # Up
        up = Vector(0, 1)
        self.assertEqual(up.mod, 1.0)
        self.assertAlmostEqual(up.theta, math.pi / 2.0)
        # Down
        down = Vector(0, -1)
        self.assertEqual(down.mod, 1.0)
        self.assertAlmostEqual(down.theta, -math.pi / 2.0)

    def test_modulo(self):
        v = Vector(3, 4)
        self.assertEqual(v.mod, 5.0)
        v = Vector(30, 0)
        self.assertEqual(v.mod, 30.0)
        v = Vector(0, 30)
        self.assertEqual(v.mod, 30.0)

    def test_modificar_modulo_no_afecta_al_angulo(self):
        v = Vector(3, 4)
        theta = v.theta
        self.assertAlmostEqual(v.mod, 5.0)
        v.mod *= 12
        self.assertAlmostEqual(v.mod, 60.0)
        self.assertAlmostEqual(v.x, 36.0)
        self.assertAlmostEqual(v.y, 48.0)
        self.assertAlmostEqual(v.theta, theta)

    def test_decremetar_modulo_no_afecta_al_angulo(self):
        v = Vector(36, 48)
        theta = v.theta
        for i in range(80):
            v.mod *= 0.95
            self.assertAlmostEqual(v.theta, theta)


    def test_get_theta(self):
        v = Vector(30, 0)
        self.assertAlmostEqual(v.theta, 0.0)
        v = Vector(30, 30)
        self.assertAlmostEqual(v.theta, math.pi / 4.0)
        v = Vector(-30, 0)
        self.assertAlmostEqual(v.theta, math.pi)

    def test_set_theta(self):
        v = Vector(3, 4)
        v.theta = 0.0
        self.assertAlmostEqual(v.x, 5.0)
        self.assertAlmostEqual(v.y, 0.0)
        v.theta = math.pi / 2.0
        self.assertAlmostEqual(v.x, 0.0)
        self.assertAlmostEqual(v.y, 5.0)

    def test_add(self): 
        v1 = Vector(3, 4)
        v2 = Vector(5, -2)
        v3 = v1 + v2
        self.assertAlmostEqual(v3.x, 8.0)
        self.assertAlmostEqual(v3.y, 2.0)

    def test_mul(self):
        v = Vector(3, 4) * 2
        self.assertAlmostEqual(v.x, 6.0)
        self.assertAlmostEqual(v.y, 8.0)

    def test_div(self):
        v = Vector(6, 8) / 2
        self.assertAlmostEqual(v.x, 3.0)
        self.assertAlmostEqual(v.y, 4.0)

    def test_equal(self):
        v1 = Vector(3, 4)
        v2 = Vector(3, 4)
        self.assertEqual(v1, v2)
        self.assertEqual(v1, (3, 4))
        self.assertEqual(v2, (3, 4))


    def test_tuple_asigment(self):
        v = Vector(3, 4)
        (a, b) = v
        self.assertEqual(a, v.x)
        self.assertEqual(b, v.y)

    def test_access_by_index(self):
        v = Vector(3, 4)
        self.assertEqual(3.0, v[0]) 
        self.assertEqual(4.0, v[1])

if __name__ == '__main__':
    unittest.main()

