import time
import unittest

import numpy as np

import enstat


class Test_binned(unittest.TestCase):
    """
    Binned data.
    """

    def test_manual(self):
        x = 0.5
        y = 1
        bin_edges = np.array([0, 1])
        binned = enstat.binned.from_data(x, y, bin_edges=bin_edges)
        self.assertTrue(np.allclose(binned[1].mean(), np.array([1])))

        x = np.array([0.5, 1.5, 2.5])
        y = np.array([1, 2, 3])
        bin_edges = np.array([0, 1, 2, 3])
        binned = enstat.binned.from_data(x, y, bin_edges=bin_edges)
        self.assertTrue(np.allclose(binned[0].mean(), np.array([0.5, 1.5, 2.5])))
        self.assertTrue(np.allclose(binned[1].mean(), np.array([1, 2, 3])))

        x = np.array([0.5, 2.5, 2.4, 2.6])
        y = np.array([1, 3, 2, 4])
        bin_edges = np.array([0, 1, 2, 3])
        notnan = np.array([True, False, True])
        binned = enstat.binned.from_data(x, y, bin_edges=bin_edges)
        self.assertTrue(np.allclose(binned[0].mean()[notnan], np.array([0.5, np.nan, 2.5])[notnan]))
        self.assertTrue(np.allclose(binned[1].mean()[notnan], np.array([1, np.nan, 3])[notnan]))

        shuffle = np.random.permutation(x.size)
        x = x[shuffle]
        y = y[shuffle]
        binned = enstat.binned.from_data(x, y, bin_edges=bin_edges)
        self.assertTrue(np.allclose(binned[0].mean()[notnan], np.array([0.5, np.nan, 2.5])[notnan]))
        self.assertTrue(np.allclose(binned[1].mean()[notnan], np.array([1, np.nan, 3])[notnan]))

        x = np.array([1.5, 2.5, 2.4, 2.6])
        y = np.array([1, 3, 2, 4])
        bin_edges = np.array([0, 1, 2, 3])
        notnan = np.array([False, True, True])
        binned = enstat.binned.from_data(x, y, bin_edges=bin_edges)
        self.assertTrue(np.allclose(binned[0].mean()[notnan], np.array([np.nan, 1.5, 2.5])[notnan]))
        self.assertTrue(np.allclose(binned[1].mean()[notnan], np.array([np.nan, 1, 3])[notnan]))

        x = np.array([2.5, 4.5])
        y = np.array([1, 2])
        bin_edges = np.array([0, 1, 2, 3, 4, 5])
        notnan = np.array([False, False, True, False, True])
        binned = enstat.binned.from_data(x, y, bin_edges=bin_edges)

    def test_bounds(self):
        x = np.array([0.5, 1.5, 2.5, 4, 5, 6])
        y = np.array([1, 2, 3, 1, 2, 3])
        bin_edges = np.array([0, 1, 2, 3])
        binned = enstat.binned.from_data(x, y, bin_edges=bin_edges, bound_error="ignore")
        self.assertTrue(np.allclose(binned[0].mean(), np.array([0.5, 1.5, 2.5])))
        self.assertTrue(np.allclose(binned[1].mean(), np.array([1, 2, 3])))

    def test_simple(self):
        """
        Plain data, one variables.
        """
        x = np.random.random(1234)
        bin_edges = np.linspace(0, 1, 13)
        binned = enstat.binned.from_data(x, bin_edges=bin_edges)

        bin = np.digitize(x.ravel(), bin_edges) - 1
        n = bin_edges.size - 1

        xmean = np.NaN * np.ones(n, dtype=float)
        xerr = np.NaN * np.ones(n, dtype=float)
        n = np.zeros(n, dtype=int)

        for ibin in range(np.max(bin) + 1):
            sel = bin == ibin
            n[ibin] = np.sum(sel)

            xi = x[sel]
            xmean[ibin] = np.mean(xi)
            xerr[ibin] = np.std(xi)

        self.assertTrue(np.allclose(binned[0].mean(), xmean))
        self.assertTrue(np.allclose(binned[0].std(), xerr, rtol=1e-2, atol=1e-5))

    def test_simple_three(self):
        """
        Plain data, three variables.
        """
        x = np.random.random(1234)
        y = np.random.random(x.shape)
        z = np.random.random(x.shape)
        bin_edges = np.linspace(0, 1, 13)
        binned = enstat.binned.from_data(x, y, z, names=["x", "y", "z"], bin_edges=bin_edges)

        bin = np.digitize(x.ravel(), bin_edges) - 1
        n = bin_edges.size - 1

        xmean = np.NaN * np.ones(n, dtype=float)
        ymean = np.NaN * np.ones(n, dtype=float)
        zmean = np.NaN * np.ones(n, dtype=float)
        xerr = np.NaN * np.ones(n, dtype=float)
        yerr = np.NaN * np.ones(n, dtype=float)
        zerr = np.NaN * np.ones(n, dtype=float)
        n = np.zeros(n, dtype=int)

        for ibin in range(np.max(bin) + 1):
            sel = bin == ibin
            n[ibin] = np.sum(sel)

            xi = x[sel]
            yi = y[sel]
            zi = z[sel]
            xmean[ibin] = np.mean(xi)
            ymean[ibin] = np.mean(yi)
            zmean[ibin] = np.mean(zi)
            xerr[ibin] = np.std(xi)
            yerr[ibin] = np.std(yi)
            zerr[ibin] = np.std(zi)

        self.assertTrue(np.allclose(binned["x"].mean(), xmean))
        self.assertTrue(np.allclose(binned["y"].mean(), ymean))
        self.assertTrue(np.allclose(binned["z"].mean(), zmean))
        self.assertTrue(np.allclose(binned["x"].std(), xerr, rtol=1e-2, atol=1e-5))
        self.assertTrue(np.allclose(binned["y"].std(), yerr, rtol=1e-2, atol=1e-5))
        self.assertTrue(np.allclose(binned["z"].std(), zerr, rtol=1e-2, atol=1e-5))

    def test_ensemble(self):
        """
        Ensemble data, two variables.
        """
        x = np.random.random([123, 11])
        y = np.random.random(x.shape)
        bin_edges = np.linspace(0, 1, 13)

        binned = enstat.binned(bin_edges)
        for i in range(x.shape[0]):
            binned.add_sample(x[i, :], y[i, :])

        bin = np.digitize(x.ravel(), bin_edges) - 1
        n = bin_edges.size - 1

        xmean = np.NaN * np.ones(n, dtype=float)
        ymean = np.NaN * np.ones(n, dtype=float)
        xerr = np.NaN * np.ones(n, dtype=float)
        yerr = np.NaN * np.ones(n, dtype=float)
        n = np.zeros(n, dtype=int)

        for ibin in range(np.max(bin) + 1):
            sel = bin == ibin
            n[ibin] = np.sum(sel)

            xi = x.ravel()[sel]
            yi = y.ravel()[sel]
            xmean[ibin] = np.mean(xi)
            ymean[ibin] = np.mean(yi)
            xerr[ibin] = np.std(xi)
            yerr[ibin] = np.std(yi)

        self.assertTrue(np.allclose(binned[0].mean(), xmean))
        self.assertTrue(np.allclose(binned[1].mean(), ymean))
        self.assertTrue(np.allclose(binned[0].std(), xerr, rtol=1e-2, atol=1e-5))
        self.assertTrue(np.allclose(binned[1].std(), yerr, rtol=1e-2, atol=1e-5))

    def test_named(self):
        """
        Ensemble data, two variables.
        """
        x = np.random.random([123, 10])
        y = np.random.random(x.shape)
        bin_edges = np.linspace(0, 1, 13)
        binned = enstat.binned(bin_edges, names=["x", "y"])
        for i in range(x.shape[0]):
            binned.add_sample(y=y[i, :], x=x[i, :])

        bin = np.digitize(x.ravel(), bin_edges) - 1
        n = bin_edges.size - 1

        xmean = np.NaN * np.ones(n, dtype=float)
        ymean = np.NaN * np.ones(n, dtype=float)
        xerr = np.NaN * np.ones(n, dtype=float)
        yerr = np.NaN * np.ones(n, dtype=float)
        n = np.zeros(n, dtype=int)

        for ibin in range(np.max(bin) + 1):
            sel = bin == ibin
            n[ibin] = np.sum(sel)

            xi = x.ravel()[sel]
            yi = y.ravel()[sel]
            xmean[ibin] = np.mean(xi)
            ymean[ibin] = np.mean(yi)
            xerr[ibin] = np.std(xi)
            yerr[ibin] = np.std(yi)

        self.assertTrue(np.allclose(binned["x"].mean(), xmean))
        self.assertTrue(np.allclose(binned["y"].mean(), ymean))
        self.assertTrue(np.allclose(binned["x"].std(), xerr, rtol=1e-2, atol=1e-5))
        self.assertTrue(np.allclose(binned["y"].std(), yerr, rtol=1e-2, atol=1e-5))

    def test_time_efficiency_dense(self):
        """
        Test efficiency of implementation of ``binned``.
        """
        bin_edges = np.linspace(0, 100000, 10000)
        a = np.random.random(int(bin_edges[-1])) * bin_edges[-1]
        bin = np.digitize(a, bin_edges) - 1

        tic = time.time()
        r0 = np.zeros(bin_edges.size - 1)
        for ibin in range(np.max(bin) + 1):
            sel = bin == ibin
            r0[ibin] = np.sum(a[sel])
        t0 = time.time() - tic

        tic = time.time()
        r1 = np.zeros(bin_edges.size - 1)
        for ibin in np.argwhere(np.bincount(bin) > 0).flatten():
            sel = bin == ibin
            r1[ibin] = np.sum(a[sel])
        t1 = time.time() - tic
        self.assertTrue(np.allclose(r0, r1))
        self.assertTrue(t0 / t1 < 2)

        tic = time.time()
        b = enstat.binned.from_data(a, bin_edges=bin_edges)
        t2 = time.time() - tic
        self.assertTrue(np.allclose(r0, b[0].first))
        self.assertLess(t2, t0)
        self.assertLess(t2, t1)

    def test_time_efficiency_sparse(self):
        """
        Test efficiency of implementation of ``binned``.
        """
        bin_edges = np.linspace(0, 100000, 10000)
        a = np.random.normal(
            size=int(bin_edges[-1]), loc=bin_edges[-1] / 2, scale=bin_edges[-1] / 100
        )
        bin = np.digitize(a, bin_edges) - 1

        tic = time.time()
        r0 = np.zeros(bin_edges.size - 1)
        for ibin in range(np.max(bin) + 1):
            sel = bin == ibin
            r0[ibin] = np.sum(a[sel])
        t0 = time.time() - tic

        tic = time.time()
        r1 = np.zeros(bin_edges.size - 1)
        for ibin in np.argwhere(np.bincount(bin) > 0).flatten():
            sel = bin == ibin
            r1[ibin] = np.sum(a[sel])
        t1 = time.time() - tic

        self.assertTrue(np.allclose(r0, r1))
        self.assertLess(t1, t0)

        tic = time.time()
        b = enstat.binned.from_data(a, bin_edges=bin_edges)
        t2 = time.time() - tic
        self.assertTrue(np.allclose(r0, b[0].first))
        self.assertLess(t2, t0)
        self.assertTrue(t2 < t1 or t2 / t1 < 1.3)


if __name__ == "__main__":
    unittest.main()
