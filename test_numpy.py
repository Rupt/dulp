"""WIP tests for numpy version
TODO description

python test_numpy.py

"""
import unittest

import numpy
from numpy import ndarray
from numpy import float32, float64
from numpy import uint32, uint64
from numpy import inf, nan

import dulp_numpy
from dulp_numpy import dulp, val, dif

f64max = numpy.finfo(float64).max
f64min = numpy.finfo(float64).tiny
f32max = numpy.finfo(float32).max
f32min = numpy.finfo(float32).tiny
u64max = uint64(2**64 - 1)
u32max = uint32(2**32 - 1)


class testdulp(unittest.TestCase):
    def test_type(self):
        self.assertIs(dulp(.5, .7).dtype.type, float32)
        self.assertIs(dulp(float32(.5), float32(.7)).dtype.type, float32)
        self.assertIsInstance(dulp([.5], [.7]), ndarray)
        self.assertIsInstance(dulp([float32(.5)], [float32(.7)]), ndarray)
        with self.assertRaises(TypeError):
            dulp(float32(1), float64(0.5))
        with self.assertRaises(TypeError):
            dulp(1j, 1j)
        with self.assertRaises(TypeError):
            dulp(0, 5e-324)

    def test_add64(self):
        self.assertEqual(dulp(1. - 2**-53, 1.), 1.)
        self.assertEqual(dulp(1.5, 1.5 + 2**-52), 1.)
        self.assertEqual(dulp(0., 5e-324), 1.)
        self.assertEqual(dulp(5e-324, 1e-323), 1.)
        self.assertEqual(dulp(f64min - 5e-324, f64min), 1.)
        self.assertEqual(dulp(-0., 0.), 1.)
        self.assertEqual(dulp(f64max, inf), 1.)

    def test_jump64(self):
        self.assertEqual(dulp(1., 1.5), 2**51.)

    def test_asym64(self):
        self.assertEqual(dulp(.5, .7), -dulp(.7, .5))
        self.assertEqual(dulp(.5, .7), -dulp(-.5, -.7))

    def test_naninf64(self):
        self.assertEqual(dulp(nan, nan), 0.)
        self.assertEqual(dulp(inf, inf), 0.)
        self.assertEqual(dulp(f64max, inf), 1.)

    def test_broadcast64(self):
        vec = dulp(.5, [.7]*2)
        mat = dulp(.5, .5*numpy.ones((1, 2, 3)))
        self.assertEqual(vec.shape, (2,))
        self.assertEqual(mat.shape, (1, 2, 3))
        self.assertEqual(vec[0], dulp(.5, .7))
        self.assertEqual(mat[0, 0, 0], 0.)
        with self.assertRaises(ValueError):
            dulp(vec, mat)

    def test_add32(self):
        self.assertEqual(dulp(float32(1. - 2**-24), float32(1.)), 1.)
        self.assertEqual(dulp(float32(1.5), float32(1.5 + 2**-23)), 1.)
        self.assertEqual(dulp(float32(0.), float32(1e-45)), 1.)
        self.assertEqual(dulp(float32(1e-45), float32(3e-45)), 1.)
        self.assertEqual(dulp(f32min - float32(1e-45), f32min), 1.)
        self.assertEqual(dulp(-float32(0.), float32(0.)), 1.)
        self.assertEqual(dulp(f32max, float32(inf)), 1.)

    def test_jump32(self):
        self.assertEqual(dulp(float32(1.), float32(1.5)), 2**22.)

    def test_asym32(self):
        self.assertEqual(dulp(float32(.5), float32(.7)),
                         -dulp(float32(.7), float32(.5)))
        self.assertEqual(dulp(float32(.5), float32(.7)),
                         -dulp(-float32(.5), -float32(.7)))

    def test_nan32(self):
        self.assertEqual(dulp(float32(nan), float32(nan)), 0.)

    def test_broadcast32(self):
        vec = dulp(.5, [.7]*2)
        mat = dulp(.5, .5*numpy.ones((1, 2, 3)))
        self.assertEqual(vec.shape, (2,))
        self.assertEqual(mat.shape, (1, 2, 3))
        self.assertEqual(vec[0], dulp(.5, .7))
        with self.assertRaises(ValueError):
            dulp(vec, mat)


class testval(unittest.TestCase):
    def test_type(self):
        self.assertIs(val(.7).dtype.type, uint64)
        self.assertIsInstance(val([.7]), ndarray)
        self.assertIs(val(float32(.7)).dtype.type, uint32)
        self.assertIsInstance(val([float32(.7)]), ndarray)
        with self.assertRaises(TypeError):
            val(-0)

    def test_ord64(self):
        self.assertLess(val(.5), val(.7))
        self.assertLess(val(-.3), val(.3))
        self.assertLess(val(0.), val(1e-323))
        self.assertLess(val(-inf), val(inf))

    def test_ord32(self):
        self.assertLess(val(float32(.5)), val(float32(.7)))
        self.assertLess(val(-float32(.3)), val(float32(.3)))
        self.assertLess(val(0.), val(1e-45))
        self.assertLess(val(-float32(inf)), val(float32(inf)))


class testdif(unittest.TestCase):
    def test_type(self):
        with self.assertRaises(TypeError):
            dif(uint32(1), uint64(1))
        with self.assertRaises(TypeError):
            dif(1, 2)

    def test_dif64(self):
        self.assertEqual(dif(uint64(0), uint64(1)), 1)
        self.assertEqual(dif(uint64(0), u64max), float32(u64max))
        self.assertEqual(dif(u64max, uint64(0)), -float32(u64max))
        self.assertEqual(dif(uint64(1), uint64(2**24 + 1)),
                         dif(uint64(0), uint64(2**24)))

    def test_dif32(self):
        self.assertEqual(dif(uint32(0), uint32(1)), 1)
        self.assertEqual(dif(uint32(0), u32max), float32(u32max))
        self.assertEqual(dif(u32max, uint32(0)), -float32(u32max))
        self.assertEqual(dif(uint32(1), uint32(2**24 + 1)),
                         dif(uint32(0), uint32(2**24)))


if __name__ == "__main__":
    unittest.main()
