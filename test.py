import unittest
import sys
import math
import dulp

from math import nan, inf, log2
from dulp import dulp, val

fmax = sys.float_info.max
fmin = sys.float_info.min


class testdulp(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(dulp(1., 1. + 2**-52), 1.)
        self.assertEqual(dulp(1.5, 1.5 + 2**-52), 1.)

    def test_jump(self):
        self.assertEqual(dulp(1., 1.5), 2.**51.)

    def test_antisym(self):
        self.assertEqual(dulp(.5, .7), -dulp(.7, .5))
        self.assertEqual(dulp(.5, .7), -dulp(-.5, -.7))

    def test_zero(self):
        self.assertEqual(dulp(-0., 0.), 1.)

    def test_denormal(self):
        self.assertEqual(dulp(0., 5e-324), 1.)
        self.assertEqual(dulp(5e-324, 1e-323), 1.)
        self.assertEqual(dulp(fmin - 5e-324, fmin), 1.)

    def test_naninf(self):
        self.assertEqual(dulp(nan, nan), 0.)
        self.assertEqual(dulp(inf, inf), 0.)
        self.assertEqual(dulp(fmax, inf), 1.)

    def test_type(self):
        self.assertIsInstance(dulp(.5, .7), float)


class testval(unittest.TestCase):
    def test_order(self):
        self.assertLess(val(.5), val(.7))
        self.assertLess(val(-.3), val(.3))
        self.assertLess(val(0.), val(1e-323))
        self.assertLess(val(-inf), val(inf))

    def test_cast(self):
        with self.assertRaises(TypeError):
            val(-0)

    def test_type(self):
        self.assertIsInstance(val(0.7), int)

    def test_arg(self):
        with self.assertRaises(TypeError):
            val(None)
        with self.assertRaises(TypeError):
            val(1j)


if __name__ == "__main__":
    unittest.main()
