import unittest
from collections import defaultdict

import numpy as np

import enstat.mean


class Test_mean(unittest.TestCase):
    """
    tests
    """

    def test_scalar(self):
        """
        Basic test of "mean" and "std" using a random sample.
        """

        average = enstat.scalar()
        average += 1.0

        self.assertFalse(np.isnan(average.mean()))
        self.assertTrue(np.isnan(average.std()))
        self.assertAlmostEqual(average.mean(), 1.0)

        average += np.array(1.0)

        self.assertFalse(np.isnan(average.mean()))
        self.assertFalse(np.isnan(average.std()))
        self.assertAlmostEqual(average.mean(), 1.0)
        self.assertAlmostEqual(average.std(), 0.0)

    def test_scalar_zero_division(self):
        """
        Check for zero division.
        """

        average = enstat.scalar()

        a = np.random.random(50 * 20).reshape(50, 20)

        for i in range(a.shape[0]):
            average += a[i, :]

        self.assertTrue(np.isclose(average.mean(), np.mean(a)))
        self.assertTrue(np.isclose(average.std(), np.std(a), rtol=1e-3))

    def test_scalar_units_div(self):
        """
        Change units.
        """

        average = enstat.scalar()

        a = np.random.random(50 * 20).reshape(50, 20)
        factor = np.random.random() + 0.1
        aprime = a / factor

        for i in range(a.shape[0]):
            average += a[i, :]

        average /= factor
        self.assertTrue(np.isclose(average.mean(), np.mean(aprime)))
        self.assertTrue(np.isclose(average.std(), np.std(aprime), rtol=1e-3))

    def test_scalar_units_mul(self):
        """
        Change units.
        """

        average = enstat.scalar()

        a = np.random.random(50 * 20).reshape(50, 20)
        factor = np.random.random() + 0.1
        aprime = a * factor

        for i in range(a.shape[0]):
            average += a[i, :]

        average *= factor
        self.assertTrue(np.isclose(average.mean(), np.mean(aprime)))
        self.assertTrue(np.isclose(average.std(), np.std(aprime), rtol=1e-3))

    def test_static(self):
        """
        Basic test of "mean" and "std" using a random sample.
        """

        average = enstat.static()

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)

        for i in range(a.shape[0]):
            average += a[i, :, :]

        self.assertTrue(np.allclose(average.mean(), np.mean(a, axis=0)))
        self.assertTrue(np.allclose(average.std(), np.std(a, axis=0), rtol=5e-1, atol=1e-3))
        self.assertTrue(average.shape == a.shape[1:])
        self.assertTrue(average.size == np.prod(a.shape[1:]))

    def test_static_units_div(self):
        """
        Change units.
        """

        average = enstat.static()

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)
        factor = np.random.random() + 0.1
        aprime = a / factor

        for i in range(a.shape[0]):
            average += a[i, :, :]

        average /= factor

        self.assertTrue(np.allclose(average.mean(), np.mean(aprime, axis=0)))
        self.assertTrue(np.allclose(average.std(), np.std(aprime, axis=0), rtol=5e-1, atol=1e-3))
        self.assertTrue(average.shape == a.shape[1:])
        self.assertTrue(average.size == np.prod(a.shape[1:]))

    def test_static_units_mul(self):
        """
        Change units.
        """

        average = enstat.static()

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)
        factor = np.random.random() + 0.1
        aprime = a * factor

        for i in range(a.shape[0]):
            average += a[i, :, :]

        average *= factor

        self.assertTrue(np.allclose(average.mean(), np.mean(aprime, axis=0)))
        self.assertTrue(np.allclose(average.std(), np.std(aprime, axis=0), rtol=5e-1, atol=1e-3))
        self.assertTrue(average.shape == a.shape[1:])
        self.assertTrue(average.size == np.prod(a.shape[1:]))

    def test_static_ravel(self):
        """
        Like :py:func:`test_static` but with a test of `ravel`.
        """

        arraylike = enstat.static()
        scalar = enstat.scalar()

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)

        for i in range(a.shape[0]):
            arraylike += a[i, :, :]
            scalar += a[i, :, :]

        flat = arraylike.ravel()

        self.assertTrue(np.allclose(flat.mean(), np.mean(a)))
        self.assertTrue(np.allclose(flat.std(), np.std(a), rtol=5e-1, atol=1e-3))
        self.assertTrue(np.allclose(flat.mean(), scalar.mean()))
        self.assertTrue(np.allclose(flat.std(), scalar.std(), rtol=5e-1, atol=1e-3))

    def test_static_division(self):
        """
        Check for zero division.
        """

        average = enstat.static()

        average += np.array([1.0])

        self.assertFalse(np.isnan(average.mean()))
        self.assertTrue(np.isnan(average.std()))

        average += np.array([1.0])

        self.assertFalse(np.isnan(average.mean()))
        self.assertFalse(np.isnan(average.std()))

    def test_static_mask(self):
        """
        Mask part of the data.
        """

        average = enstat.static()

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)
        m = np.random.random(35 * 50 * 20).reshape(35, 50, 20) > 0.8

        for i in range(a.shape[0]):
            average.add_sample(a[i, :, :], m[i, :, :])

        self.assertTrue(
            np.isclose(
                np.sum(average.first) / np.sum(average.norm),
                np.mean(a[np.logical_not(m)]),
            )
        )

        self.assertTrue(
            np.isclose(
                np.sum(average.first) / np.sum(average.norm),
                np.mean(a[np.logical_not(m)]),
            )
        )

        self.assertTrue(np.all(np.equal(average.norm, np.sum(np.logical_not(m), axis=0))))

    def test_static_add_point(self):
        """
        Add data point-by-point.
        """

        a = np.random.random(35 * 50).reshape(35, 50)
        m = np.random.random(35 * 50).reshape(35, 50) > 0.8
        average = enstat.static(shape=a.shape[1])

        for i in range(a.shape[0]):
            for j in np.argwhere(~m[i, :]).ravel():
                average.add_point(a[i, j], j)

        self.assertTrue(
            np.isclose(
                np.sum(average.first) / np.sum(average.norm),
                np.mean(a[np.logical_not(m)]),
            )
        )

        self.assertTrue(
            np.isclose(
                np.sum(average.first) / np.sum(average.norm),
                np.mean(a[np.logical_not(m)]),
            )
        )

        self.assertTrue(np.all(np.equal(average.norm, np.sum(np.logical_not(m), axis=0))))

    def test_static_squash_example(self):
        norm = np.array([[2, 2, 3, 1, 1], [2, 2, 1, 1, 3], [1, 1, 2, 2, 1], [2, 1, 2, 2, 2]])
        average = enstat.static(shape=norm.shape)
        average.norm = norm
        average.squash([2, 2])
        expect = np.array([[8, 6, 4], [5, 8, 3]])
        self.assertTrue(np.all(np.equal(average.norm, expect)))

    def test_static_squash_1d_a(self):
        a = np.random.random(13 * 2).reshape(13, 2)
        average = enstat.static(shape=[a.size])
        average += a.ravel()
        average.squash(2)
        self.assertTrue(np.allclose(average.mean(), np.mean(a, axis=1)))

        e = np.random.random(1)
        average = enstat.static(shape=[a.size + 1])
        average += np.concatenate((a.ravel(), e))
        average.squash(2)
        self.assertTrue(np.allclose(average.mean(), np.concatenate((np.mean(a, axis=1), e))))

    def test_static_squash_1d_b(self):
        a = np.random.random(13 * 3).reshape(13, 3)
        average = enstat.static(shape=[a.size])
        average += a.ravel()
        average.squash(3)
        self.assertTrue(np.allclose(average.mean(), np.mean(a, axis=1)))

        e = np.random.random(2)
        average = enstat.static(shape=[a.size + 2])
        average += np.concatenate((a.ravel(), e))
        average.squash(3)
        self.assertTrue(
            np.allclose(
                average.mean(), np.concatenate((np.mean(a, axis=1), np.array([np.mean(e)])))
            )
        )

    def test_static_squash_2d_a(self):
        a = np.random.random(12 * 8).reshape(12, 8)
        b = 0.25 * (a[::2, ::2] + a[1::2, ::2] + a[::2, 1::2] + a[1::2, 1::2])
        average = enstat.static(shape=a.shape)
        average += a
        average.squash([2, 2])
        self.assertTrue(np.allclose(average.mean(), b))

        a = np.random.random(12 * 8).reshape(12, 8)[:-1, :]
        n = np.ones_like(a)
        z = np.zeros((1, 4))
        b = (
            a[::2, ::2]
            + np.vstack((a[1::2, ::2], z))
            + a[::2, 1::2]
            + np.vstack((a[1::2, 1::2], z))
        )
        n = (
            n[::2, ::2]
            + np.vstack((n[1::2, ::2], z))
            + n[::2, 1::2]
            + np.vstack((n[1::2, 1::2], z))
        )
        average = enstat.static(shape=a.shape)
        average += a
        average.squash([2, 2])
        self.assertTrue(np.allclose(average.mean(), b / n))

        a = np.random.random(12 * 8).reshape(12, 8)[:, :-1]
        n = np.ones_like(a)
        z = np.zeros((6, 1))
        b = (
            a[::2, ::2]
            + a[1::2, ::2]
            + np.hstack((a[::2, 1::2], z))
            + np.hstack((a[1::2, 1::2], z))
        )
        n = (
            n[::2, ::2]
            + n[1::2, ::2]
            + np.hstack((n[::2, 1::2], z))
            + np.hstack((n[1::2, 1::2], z))
        )
        average = enstat.static(shape=a.shape)
        average += a
        average.squash([2, 2])
        self.assertTrue(np.allclose(average.mean(), b / n))

        a = np.random.random(12 * 8).reshape(12, 8)[:-1, :-1]
        n = np.ones_like(a)
        zr = np.zeros((1, 4))
        zc = np.zeros((6, 1))
        zc1 = np.zeros((5, 1))
        b = (
            a[::2, ::2]
            + np.vstack((a[1::2, ::2], zr))
            + np.hstack((a[::2, 1::2], zc))
            + np.vstack((np.hstack((a[1::2, 1::2], zc1)), zr))
        )
        n = (
            n[::2, ::2]
            + np.vstack((n[1::2, ::2], zr))
            + np.hstack((n[::2, 1::2], zc))
            + np.vstack((np.hstack((n[1::2, 1::2], zc1)), zr))
        )
        average = enstat.static(shape=a.shape)
        average += a
        average.squash([2, 2])
        self.assertTrue(np.allclose(average.mean(), b / n))

    def test_dynamic1d(self):
        """
        Dynamically grow shape.
        """

        average = enstat.dynamic1d()

        average += np.array([1, 2, 3])
        average += np.array([1, 2, 3])
        average += np.array([1, 2])
        average += np.array([1])
        average += np.array([1, 2, 3, 4])
        average += np.array([1, 2, 3, 4])

        self.assertTrue(np.allclose(average.mean(), np.array([1, 2, 3, 4])))
        self.assertTrue(np.allclose(average.std(), np.array([0, 0, 0, 0])))
        self.assertEqual(average.shape, (4,))
        self.assertEqual(average.size, 4)


class Test_defaultdict(unittest.TestCase):
    """
    functionality
    """

    def test_scalar(self):
        average = defaultdict(enstat.scalar)

        a = np.random.random(50 * 20).reshape(50, 20)
        b = np.random.random(52 * 21).reshape(52, 21)

        for i in range(a.shape[0]):
            average["a"] += a[i, :]

        for i in range(b.shape[0]):
            average["b"] += b[i, :]

        self.assertTrue(np.isclose(average["a"].mean(), np.mean(a)))
        self.assertTrue(np.isclose(average["b"].mean(), np.mean(b)))

    def test_static(self):
        average = defaultdict(enstat.static)

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)
        b = np.random.random(37 * 52 * 21).reshape(37, 52, 21)

        for i in range(a.shape[0]):
            average["a"] += a[i, :, :]

        for i in range(b.shape[0]):
            average["b"] += b[i, :, :]

        self.assertTrue(np.allclose(average["a"].mean(), np.mean(a, axis=0)))
        self.assertTrue(np.allclose(average["b"].mean(), np.mean(b, axis=0)))
        self.assertTrue(average["a"].shape == a.shape[1:])
        self.assertTrue(average["b"].shape == b.shape[1:])


class Test_restore(unittest.TestCase):
    """
    Restore existing average.
    """

    def test_scalar(self):
        data = np.random.random(100)
        average = enstat.scalar()

        for i in data:
            average += i

        restored = enstat.scalar.restore(**dict(average))

        self.assertTrue(np.isclose(average.first, restored.first))
        self.assertTrue(np.isclose(average.second, restored.second))
        self.assertTrue(average.norm == restored.norm)

        self.assertTrue(np.isclose(np.mean(data), average.mean()))
        self.assertTrue(np.isclose(np.std(data), average.std(), rtol=5e-1, atol=1e-3))

        self.assertTrue(np.isclose(np.mean(data), restored.mean()))
        self.assertTrue(np.isclose(np.std(data), restored.std(), rtol=5e-1, atol=1e-3))

    def test_static(self):
        data = np.random.random(31 * 50 * 11).reshape(31, 50, 11)
        average = enstat.static()

        for i in range(data.shape[0]):
            average += data[i, ...]

        restored = enstat.static.restore(**dict(average))

        self.assertTrue(np.allclose(average.first, restored.first))
        self.assertTrue(np.allclose(average.second, restored.second))
        self.assertTrue(np.all(average.norm == restored.norm))

        self.assertTrue(np.allclose(np.mean(data, axis=0), average.mean()))
        self.assertTrue(np.allclose(np.std(data, axis=0), average.std(), rtol=5e-1, atol=1e-3))

        self.assertTrue(np.allclose(np.mean(data, axis=0), restored.mean()))
        self.assertTrue(np.allclose(np.std(data, axis=0), restored.std(), rtol=5e-1, atol=1e-3))

    def test_dynamic1d(self):
        data = np.random.random(31 * 50).reshape(31, 50)
        average = enstat.dynamic1d()

        for i in data:
            average += i

        restored = enstat.dynamic1d.restore(**dict(average))

        self.assertTrue(np.allclose(average.first, restored.first))
        self.assertTrue(np.allclose(average.second, restored.second))
        self.assertTrue(np.all(average.norm == restored.norm))

        self.assertTrue(np.allclose(np.mean(data, axis=0), average.mean()))
        self.assertTrue(np.allclose(np.std(data, axis=0), average.std(), rtol=5e-1, atol=1e-3))

        self.assertTrue(np.allclose(np.mean(data, axis=0), restored.mean()))
        self.assertTrue(np.allclose(np.std(data, axis=0), restored.std(), rtol=5e-1, atol=1e-3))


if __name__ == "__main__":
    unittest.main()
