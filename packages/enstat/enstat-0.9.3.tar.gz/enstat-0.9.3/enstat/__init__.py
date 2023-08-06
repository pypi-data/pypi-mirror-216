from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike
from numpy.typing import DTypeLike

from . import detail  # noqa: F401
from . import mean  # noqa: F401
from ._version import version  # noqa: F401
from ._version import version_tuple  # noqa: F401


class scalar:
    r"""
    Ensemble average of a scalar.
    Example:

    .. code-block:: python

        import enstat

        average = enstat.scalar()
        average += 1.0
        average += 2.0
        average += 3.0
        print(average.mean())  # 2.0

    Add samples to it using :py:func:`scalar.add_sample`, or simply `average += datum`.
    The mean, variance, and standard deviation can be obtained at any time.
    They are derived from the following members:

    *   :py:attr:`scalar.first`: Sum of the first statistical moment.
    *   :py:attr:`scalar.second`: Sum of the second statistical moment.
    *   :py:attr:`scalar.norm`: Number of samples.

    To restore data: use :py:func:`scalar.restore`.
    In short: `restored = enstat.scalar.restore(**dict(average))`.
    """

    def __init__(self):
        self.first = 0.0
        self.second = 0.0
        self.norm = 0.0

    def __iter__(self):
        yield "first", self.first
        yield "second", self.second
        yield "norm", self.norm

    @classmethod
    def restore(cls, first: float = 0, second: float = 0, norm: float = 0):
        """
        Restore previous data.

        :param float first: Sum of the first moment.
        :param float second: Sum of the second moment.
        :param int norm: Number of samples.
        """

        ret = cls()
        ret.first = first
        ret.second = second
        ret.norm = norm
        return ret

    def __add__(self, datum: float | ArrayLike):
        self.add_sample(datum)
        return self

    def __itruediv__(self, factor: float):
        assert not hasattr(factor, "__len__")
        self.first /= factor
        self.second /= factor**2
        return self

    def __imul__(self, factor: float):
        assert not hasattr(factor, "__len__")
        self.first *= factor
        self.second *= factor**2
        return self

    def add_sample(self, datum: float | ArrayLike):
        """
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.

        :param datum: Sample.
        """

        datum = np.array(datum)
        self.first += np.sum(datum)
        self.second += np.sum(datum**2)
        self.norm += datum.size

    def mean(self) -> float:
        r"""
        Current mean.
        Samples can be added afterwards without any problems.

        :return: Mean.
        """

        if self.norm == 0:
            return np.NaN

        return self.first / self.norm

    def variance(self) -> float:
        r"""
        Current variance.
        Samples can be added afterwards without any problems.

        :return: Variance.
        """

        if self.norm <= 1:
            return np.NaN

        d = (self.second / self.norm - (self.first / self.norm) ** 2) * self.norm
        n = self.norm - 1

        return d / n

    def std(self) -> float:
        r"""
        Current standard deviation.
        Samples can be added afterwards without any problems.

        :return: Standard deviation.
        """

        return np.sqrt(self.variance())


class static:
    r"""
    Ensemble average of an nd-array (of same size for all samples).
    .. code-block:: python

        import enstat
        import numpy as np

        data = np.random.random(35 * 50).reshape(35, 50)

        average = enstat.static()
        for datum in data:
            average += datum
        print(average.mean())  # approximately [0.5, 0.5, ...]

    Add samples to it using :py:func:`static.add_sample`, or simply `average += datum`.
    The mean, variance, and standard deviation can be obtained at any time.
    They are derived from the following members:

    *   :py:attr:`static.first`: Sum of the first statistical moment.
    *   :py:attr:`static.second`: Sum of the second statistical moment.
    *   :py:attr:`static.norm`: Number of samples.

    To restore data: use :py:func:`static.restore`.
    In short: `restored = enstat.static.restore(**dict(average))`.

    For convenience, the following members are available:

    *   :py:attr:`static.shape`: Shape of the data.
    *   :py:attr:`static.size`: Size of the data (= prod(shape)).

    :param compute_variance:
        If set ``False`` no second moment will be computed (making things slightly faster).
        In that case, the variance an standard deviation will not be available.

    :param shape:
        The shape of the data.
        If not specified it is determined form the first sample.

    :param dtype:
        The type of the data.
        If not specified it is determined form the first sample.
    """

    def __init__(
        self,
        compute_variance: bool = True,
        shape: tuple[int] = None,
        dtype: DTypeLike = np.float64,
    ):
        self.compute_variance = compute_variance
        self.norm = None
        self.first = None
        self.second = None

        if shape is None:
            return

        self.norm = np.zeros(shape, np.int64)
        self.first = np.zeros(shape, dtype)
        if compute_variance:
            self.second = np.zeros(shape, dtype)

    def __iter__(self):
        yield "first", self.first
        yield "second", self.second
        yield "norm", self.norm

    @classmethod
    def restore(
        cls,
        first: ArrayLike = None,
        second: ArrayLike = None,
        norm: ArrayLike = None,
    ):
        """
        Restore previous data.

        :param first: Continued computation: Sum of the first moment.
        :param second: Continued computation: Sum of the second moment.
        :param norm: Continued computation: Number of samples (integer).
        """

        if norm is not None:
            assert first is not None
            assert first.shape == norm.shape

            if second is not None:
                assert second.shape == norm.shape

        ret = cls()
        ret.first = first
        ret.second = second
        ret.norm = norm
        return ret

    def _allocate(self, shape, dtype):
        self.norm = np.zeros(shape, np.int64)
        self.first = np.zeros(shape, dtype)
        if self.compute_variance:
            self.second = np.zeros(shape, dtype)

    @property
    def dtype(self):
        """
        The type of the data.
        """
        return self.first.dtype

    @property
    def shape(self):
        """
        The shape of the data.
        """
        return self.first.shape

    @property
    def size(self):
        """
        The size of the data.
        """
        return np.prod(self.first.shape)

    def ravel(self) -> scalar:
        r"""
        Return as :py:class:`scalar`: all entries are summed.

        :return: Ensemble average.
        """

        return scalar.restore(
            first=np.sum(self.first),
            second=np.sum(self.second),
            norm=np.sum(self.norm),
        )

    def __add__(self, data: ArrayLike):
        self.add_sample(data)
        return self

    def __itruediv__(self, factor: float | ArrayLike):
        if hasattr(factor, "__len__"):
            assert factor.shape == self.first.shape
        self.first /= factor
        if self.second is not None:
            self.second /= factor**2
        return self

    def __imul__(self, factor: float | ArrayLike):
        if hasattr(factor, "__len__"):
            assert factor.shape == self.first.shape
        self.first *= factor
        if self.second is not None:
            self.second *= factor**2
        return self

    def add_sample(self, data: ArrayLike, mask: ArrayLike = None):
        r"""
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.

        :param data: The sample.
        :param mask: Mask entries (boolean array).
        """

        if self.first is None:
            self._allocate(data.shape, data.dtype)

        # masked data
        if mask is not None:
            incl = np.logical_not(mask)
            self.norm[incl] += 1
            self.first[incl] += data[incl]
            if self.compute_variance:
                self.second[incl] += data[incl] ** 2
            return

        # unmasked data
        self.norm += 1
        self.first += data
        if self.compute_variance:
            self.second += data**2

    def add_point(self, datum: float | int, index: int):
        """
        Add a single point. Note that::

            ensemble.add_point(datum, index)

        Is equivalent to::

            data = np.empty(ensemble.shape)
            mask = np.ones(ensemble.shape, dtype=bool)
            data[index] = datum
            mask[index] = False
            ensemble.add_sample(data, mask)

        (but faster).
        """

        if self.first is None:
            raise OSError("shape should be pre-specified")

        self.norm[index] += 1
        self.first[index] += datum

        if self.compute_variance:
            self.second[index] += datum**2

    def mean(self, min_norm: int = 1) -> ArrayLike:
        r"""
        Current mean.
        Samples can be added afterwards without any problems.

        :param min_norm: Minimum number of samples to consider as value output.
        :return: Mean.
        """

        if self.norm is None:
            return None

        n = np.where(self.norm > 0, self.norm, 1)
        ret = self.first / n
        return np.where(self.norm >= min_norm, ret, np.NaN)

    def variance(self, min_norm: int = 2) -> ArrayLike:
        r"""
        Current variance.
        Samples can be added afterwards without any problems.

        :param min_norm: Minimum number of samples to consider as value output.
        :return: Variance.
        """

        if self.norm is None:
            return None

        assert self.compute_variance
        n = np.where(self.norm > 1, self.norm, 2)
        ret = (self.second / n - (self.first / n) ** 2) * n / (n - 1)
        return np.where(self.norm >= min_norm, ret, np.NaN)

    def std(self, min_norm: int = 2) -> ArrayLike:
        r"""
        Current standard deviation.
        Samples can be added afterwards without any problems.

        :param min_norm: Minimum number of samples to consider as value output.
        :return: Standard deviation.
        """

        if self.norm is None:
            return None

        return np.sqrt(self.variance(min_norm))

    def squash(self, n: int | list[int]):
        """
        Squash the data to a smaller size by summing over blocks of size ``n``.
        For example, suppose that::

            >>> avg.norm
            [[2, 2, 3, 1, 1],
             [2, 2, 1, 1, 3],
             [1, 1, 2, 2, 1],
             [2, 1, 2, 2, 2]]

        Then calling::

            >>> avg.squash(2)
            >>> avg.norm
            [[8, 6, 4],
             [5, 8, 3]]
        """
        assert self.norm is not None, "no data yet"

        if not hasattr(n, "__len__"):
            n = [n]

        assert self.norm.ndim == len(n)

        for i in range(len(n)):
            iter = np.arange(0, self.norm.shape[i], n[i])
            self.norm = np.add.reduceat(self.norm, iter, axis=i)
            self.first = np.add.reduceat(self.first, iter, axis=i)
            if self.compute_variance:
                self.second = np.add.reduceat(self.second, iter, axis=i)


def _expand_array1d(data, size):
    tmp = np.zeros((size), data.dtype)
    tmp[: data.size] = data
    return tmp


class dynamic1d(static):
    r"""
    Ensemble average of an 1d-array (which grows depending of the size of the samples).
    Add samples to it using :py:func:`dynamic1d.add_sample`, or simply `average += datum`.
    The mean, variance, and standard deviation can be obtained at any time.
    Also the sums of the first and statistical moments, as well as the number of samples can be
    obtained at any time.

    To restore data: use :py:func:`dynamic1d.restore`.
    In short: `restored = enstat.dynamic1d.restore(**dict(average))`.

    :param compute_variance:
        If set ``False`` no second moment will be computed.
        In that case, the variance an standard deviation will not be available.

    :param size:
        The initial size of the data.
        If not specified it is determined form the first sample.

    :param dtype:
        The type of the data.
        If not specified it is determined form the first sample.
    """

    def __init__(
        self,
        compute_variance: bool = True,
        size: int = None,
        dtype: DTypeLike = np.float64,
    ):
        super().__init__(
            compute_variance=compute_variance,
            shape=(size,) if size is not None else None,
            dtype=dtype,
        )

    def _expand(self, size: int):
        if size <= self.first.size:
            return

        self.norm = _expand_array1d(self.norm, size)
        self.first = _expand_array1d(self.first, size)

        if self.compute_variance:
            self.second = _expand_array1d(self.second, size)

    def __add__(self, data: ArrayLike):
        self.add_sample(data)
        return self

    def add_sample(self, data: ArrayLike):
        assert data.ndim == 1

        if self.first is None:
            super().add_sample(data)
            return

        self._expand(data.size)
        self.norm[: data.size] += 1
        self.first[: data.size] += data

        if self.compute_variance:
            self.second[: data.size] += data**2

    def add_point(self, datum: float | int, index: int):
        if self.first is None:
            self._allocate(index + 1, type(datum))
        else:
            self._expand(index + 1)

        return super().add_point(datum, index)


class histogram:
    """
    Histogram.
    Example single dataset:

    .. code-block:: python

        data = [0, 0, 0, 1, 1, 2]
        bin_edges = [-0.5, 0.5, 1.5, 2.5]
        hist = enstat.histogram.from_data(data, bin_edges)
        print(hist.count)

    Example ensemble:

    .. code-block:: python

        data = np.random.random(35 * 50).reshape(35, 50)
        bin_edges = np.linspace(0, 1, 11)
        hist = enstat.histogram(bin_edges)

        for datum in data:
            hist += datum

        print(hist.count)

    One can add samples to it using :py:func:`Histogram.add_sample`, or simply `hist += datum`.

    Members:

    *   :py:attr:`scalar.count`: The number of samples in each bin.
    *   :py:attr:`scalar.bin_edges`: See option ``bin_edges``.
    *   :py:attr:`scalar.x`: Midpoint of each bin.
    *   :py:attr:`scalar.p`: Probability density of each bin.
    *   :py:attr:`scalar.right`: See option ``right``.
    *   :py:attr:`scalar.bound_error`: See option ``bound_error``
    *   :py:attr:`scalar.count_left`: Number of samples that fall below the leftmost bin.
    *   :py:attr:`scalar.count_right`: Number of samples that fall above the rightmost bin.

    :param bin_edges: The bin-edges.
    :param right: Whether the bin includes the right edge (or the left edge) see numpy.digitize.
    :param bound_error: What to do if a sample falls out of the bin range:

        - ``"raise"``: raise an error
        - ``"ignore"``: ignore the data that are out of range
        - ``"norm"``: change the normalisation of the density
    """

    def __init__(
        self,
        bin_edges: ArrayLike,
        right: bool = False,
        bound_error: str = "raise",
    ):
        assert np.all(np.diff(bin_edges) > 0) or np.all(np.diff(bin_edges) < 0)

        self.right = right
        self.bin_edges = np.array(bin_edges).astype(np.float64)
        self.bound_error = bound_error
        self.count_left = 0
        self.count_right = 0
        self.bound_left = bin_edges[0]
        self.bound_right = bin_edges[-1]
        self.count = np.zeros((len(bin_edges) - 1), np.uint64)

        if bound_error not in {"raise", "ignore", "norm"}:
            raise ValueError(f"Unknown bound_error: {bound_error}")

    def __iter__(self):
        yield "bin_edges", self.bin_edges
        yield "count", self.count
        yield "count_left", self.count_left
        yield "count_right", self.count_right
        yield "bound_left", self.bound_left
        yield "bound_right", self.bound_right
        yield "right", self.right
        yield "bound_error", self.bound_error

    @classmethod
    def restore(
        cls,
        bin_edges: ArrayLike,
        count: ArrayLike,
        count_left: int = 0,
        count_right: int = 0,
        bound_left: float = None,
        bound_right: float = None,
        bound_error: str = "raise",
        right: bool = False,
    ):
        """
        Restore from a previous result::

            hist = enstat.histogram...
            state = dict(hist)

            restored = enstat.histogram.from_histogram(**state)

        :param bin_edges: The bin-edges.
        :param count: The count.
        :param count_left: Number of items below the left bound.
        :param count_right: Number of items above the right bound.
        :param bound_left: The minimum value below the left bound.
        :param bound_right: The maximum value above the right bound.
        :param bound_error: What to do if a sample falls out of the bin range.
        :param right: Whether the bin includes the right edge (or the left edge) see numpy.digitize.
        """

        ret = cls(
            bin_edges=bin_edges,
            right=right,
            bound_error=bound_error,
        )

        assert len(count) == len(bin_edges) - 1
        ret.count = np.array(count).astype(np.uint64)

        ret.count_left = count_left
        ret.count_right = count_right

        if bound_left is not None:
            assert bound_left <= bin_edges[0]
            ret.bound_left = bound_left

        if bound_right is not None:
            assert bound_right >= bin_edges[-1]
            ret.bound_right = bound_right

        return ret

    @classmethod
    def from_data(
        cls,
        data: ArrayLike,
        bins: int = None,
        mode: str = "equal",
        min_count: int = None,
        min_width: float = None,
        integer: bool = False,
        bin_edges: ArrayLike = None,
        bound_error: str = "raise",
    ):
        r"""
        Construct a histogram from data.

        :param data: Data (flattened).
        :param bins: Number of bins.
        :param mode:
            Mode with which to compute the bin-edges.

            -   ``'equal'``: each bin has equal width.
            -   ``'log'``: logarithmic spacing.
            -   ``'uniform'``: uniform number of data-points per bin.
            -   ``'voronoi'``: each bin is the region between two adjacent data-points.

        :param min_count: Minimum number of data-points per bin.
        :param min_width: Minimum width of a bin.

        :param integer:
            If ``True``, bins not encompassing an integer are removed
            (e.g. a bin with edges ``[1.1, 1.9]`` is removed, but ``[0.9, 1.1]`` is not removed).

        :param bin_edges: Specify the bin-edges (overrides ``bins`` and ``mode``).

        :param bound_error: What to do if a sample falls out of the bin range:

            - ``"raise"``: raise an error
            - ``"ignore"``: ignore the data that are out of range
            - ``"norm"``: change the normalisation of the density

        :return: The :py:class:`Histogram` object.
        """

        data = np.asarray(data)

        if hasattr(bins, "__len__"):
            raise OSError("Only the number of bins can be specified")

        if bin_edges is None:
            bin_edges = detail.histogram_bin_edges(data, bins, mode, min_count)

        if min_count is not None:
            bin_edges = detail.histogram_bin_edges_mincount(data, bin_edges, min_count)

        if min_width is not None:
            bin_edges = detail.histogram_bin_edges_minwidth(bin_edges, min_width)

        if integer:
            bin_edges = detail.histogram_bin_edges_integer(bin_edges)

        d = bin_edges[-1] - bin_edges[0]
        bin_edges[0] = np.nextafter(bin_edges[0], bin_edges[0] - d)
        bin_edges[-1] = np.nextafter(bin_edges[-1], bin_edges[-1] + d)
        return cls(bin_edges, right=True, bound_error=bound_error).add_sample(data)

    def strip(self, min_count: int = 0):
        """
        Strip the histogram of empty bins to the left and the right.

        :param min_count: The minimum count for a bin to be considered non-empty.
        """

        self.lstrip(min_count)
        self.rstrip(min_count)
        return self

    def lstrip(self, min_count: int = 0):
        """
        Strip the histogram of empty bins to the left.

        :param min_count: The minimum count for a bin to be considered non-empty.
        """

        i = np.argmax(self.count > min_count)
        self.count = self.count[i:]
        self.bin_edges = self.bin_edges[i:]
        return self

    def rstrip(self, min_count: int = 0):
        """
        Strip the histogram of empty bins to the right.

        :param min_count: The minimum count for a bin to be considered non-empty.
        """

        i = len(self.count) - np.argmax(self.count[::-1] > min_count)
        self.count = self.count[:i]
        self.bin_edges = self.bin_edges[: i + 1]
        return self

    def interp(self, bin_edges: ArrayLike):
        """
        Interpolate the histogram to a new set of bin-edges.

        :param bin_edges: The new bin-edges.
        """

        assert np.all(np.diff(bin_edges) > 0) or np.all(np.diff(bin_edges) < 0)

        m = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        self.count = np.interp(m, self.x, self.count)
        self.bin_edges = bin_edges
        return self

    def squash(self, n: int):
        """
        Squash the histogram by combining ``n`` sequential bins into one
        (the last bin may be smaller).

        :param n: Number of bins to group.
        """

        if n >= self.count.size:
            self.count = np.sum(self.count).reshape(1)
            self.bin_edges = self.bin_edges[[0, -1]]
            return self

        m = self.count.size // n
        s = m * n
        self.count = np.hstack((self.count[:s].reshape((m, n)).sum(axis=1), np.sum(self.count[s:])))

        if len(self.bin_edges) // n != self.count.size + 1:
            self.bin_edges = np.hstack((self.bin_edges[::n], self.bin_edges[-1]))
        else:
            self.bin_edges = self.bin_edges[::n]

        return self

    def merge_right(self, index: ArrayLike):
        """
        Merge the bins to the right of ``index`` into ``index``.

        :param index: The indices of the bin to merge into.
        """

        if isinstance(index, int):
            index = [index]

        index = np.array(index)
        index = np.sort(np.where(index < 0, index + self.count.size, index))

        if index[-1] == self.count.size - 1:
            index = index[:-1]

        self.count[index] += self.count[index + 1]
        self.count = np.delete(self.count, index + 1)
        self.bin_edges = np.delete(self.bin_edges, index + 1)
        return self

    def merge_left(self, index: ArrayLike):
        """
        Merge the bins to the left of ``index`` into ``index``.

        :param index: The indices of the bin to merge into.
        """

        if isinstance(index, int):
            index = [index]

        index = np.array(index)
        index = np.sort(np.where(index < 0, index + self.count.size, index))

        if index[0] == 0:
            index = index[1:]

        self.count[index - 1] += self.count[index]
        self.count = np.delete(self.count, index)
        self.bin_edges = np.delete(self.bin_edges, index)
        return self

    def as_integer(self):
        """
        Merge bins not encompassing an integer with the preceding bin.
        For example: a bin with edges ``[1.1, 1.9]`` is removed, but ``[0.9, 1.1]`` is not removed.
        """

        assert self.bin_edges.size > 1

        merge = np.argwhere(np.diff(np.floor(self.bin_edges)) == 0).ravel()
        self.merge_right(merge)
        self.bin_edges = np.floor(self.bin_edges)
        self.right = False

    def __add__(self, data: ArrayLike):
        self.add_sample(data)
        return self

    def _get_bins(self, data: ArrayLike, return_selector: bool = False) -> np.ndarray[int]:
        """
        Get the bins for the data, update out-of-range counts.
        """

        data = np.asarray(data)
        bin = np.digitize(data, self.bin_edges, right=self.right) - 1
        left = data < self.bin_edges[0]
        right = data >= self.bin_edges[-1]
        nleft = np.sum(left)
        nright = np.sum(right)
        self.count_left += nleft
        self.count_right += nright

        if nleft:
            self.bound_left = min([self.bound_left, np.min(data[left])])

        if nright:
            self.bound_right = max([self.bound_right, np.max(data[right])])

        if self.bound_error == "raise" and (nleft or nright):
            raise ValueError("Data out of bin range")

        if return_selector:
            keep = np.logical_and(~left, ~right)
            return bin[keep], keep

        return bin[np.logical_and(~left, ~right)]

    def add_sample(self, data: ArrayLike):
        """
        Add a sample to the histogram.
        You can also use the ``+`` operator.
        """
        self.count += np.bincount(self._get_bins(data), minlength=self.count.size).astype(np.uint64)
        return self

    @property
    def x(self) -> ArrayLike:
        """
        The bin centers.
        """
        return 0.5 * (self.bin_edges[:-1] + self.bin_edges[1:])

    @property
    def density(self) -> ArrayLike:
        """
        The probability density function at the bin.
        """
        count = self.count.astype(np.float64)
        norm = np.sum(count)

        if self.bound_error == "norm":
            norm += self.count_left + self.count_right

        return count / (np.diff(self.bin_edges) * norm)

    @property
    def p(self) -> ArrayLike:
        """
        The probability density function at the bin.
        """
        return self.density

    @property
    def plot(self) -> tuple[ArrayLike, ArrayLike]:
        """
        Alias for ``(x, density)``.
        """
        return (self.x, self.density)


class binned:
    """
    Ensemble average after binning.
    Example:

    .. code-block:: python

        import numpy as np
        import enstat

        x = np.array([0.5, 1.5, 2.5])
        y = np.array([1, 2, 3])
        bin_edges = np.array([0, 1, 2, 3])
        binned = enstat.binned.from_data(x, y, bin_edges=bin_edges)
        print(binned[0].mean())

    :param bin_edges: The bin-edges.
    :param right: Whether the bin includes the right edge (or the left edge) see numpy.digitize.
    :param bound_error: What to do if a sample falls out of the bin range:

        - ``"raise"``: raise an error
        - ``"ignore"``: ignore the data that are out of range

    :param names: The names of the variables to store.
    """

    def __init__(
        self,
        bin_edges: ArrayLike,
        right: bool = False,
        bound_error: str = "raise",
        names: list[str] = [],
    ):
        self.hist = histogram(bin_edges, right, bound_error)
        self.names = names
        self.data = {name: static(shape=self.hist.bin_edges.size - 1) for name in names}
        if bound_error not in {"raise", "ignore"}:
            raise ValueError(f"Unknown bound_error: {bound_error}")

    @classmethod
    def from_data(cls, *args: ArrayLike, names: list[str] = [], **kwargs):
        r"""
        Construct from data.

        :param args:
            Different variables of data to add.
            The binning is done on the first argument and applied to all other arguments.

        :param kwargs: Automatic binning settings, see :py:meth:`histogram.from_data`.
        :return: The :py:class:`Histogram` object.
        """

        hist = histogram.from_data(args[0], **kwargs)
        return cls(
            hist.bin_edges, right=hist.right, bound_error=hist.bound_error, names=names
        ).add_sample(*args)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index: int):
        if isinstance(index, str):
            return self.data[index]
        return self.data[self.names[index]]

    def __add__(self, data: ArrayLike):
        self.add_sample(data)
        return self

    def add_sample(self, *args: ArrayLike, **kwargs: ArrayLike):
        """
        Add a sample.
        If you use only one variable, you can also use the ``+`` operator.

        :param args:
            Different variables of data to add.
            The binning is done on the first argument and applied to all other arguments.
        """

        if len(self.names) == 0:
            self.names = [i for i in range(len(args))]
            self.data = {name: static(shape=self.hist.bin_edges.size - 1) for name in self.names}

        for i in range(len(args)):
            name = self.names[i]
            if name in kwargs:
                raise ValueError(f"Duplicate argument: {name}")
            kwargs[name] = args[i]

        if len(kwargs) != len(self.names):
            raise ValueError("Incorrect number of arguments")

        ibin, keep = self.hist._get_bins(kwargs[self.names[0]], return_selector=True)
        kwargs = {name: np.asarray(arg)[keep] for name, arg in kwargs.items()}
        sqr = {name: arg * arg for name, arg in kwargs.items()}

        for name, arg in kwargs.items():
            if arg.shape != kwargs[self.names[0]].shape:
                raise ValueError("All arguments must have the same shape")

        # see https://stackoverflow.com/q/76574134/2646505
        sorter = np.argsort(ibin)
        ibin = ibin[sorter]
        norm = np.argwhere(np.diff(ibin, prepend=ibin[0], append=1)).flatten()
        split = norm - 1
        norm = np.diff(norm, prepend=0)
        store = ibin[split]

        for name, arg in kwargs.items():
            self.data[name].first[store] += np.diff(np.cumsum(arg[sorter])[split], prepend=0)
            self.data[name].second[store] += np.diff(np.cumsum(sqr[name][sorter])[split], prepend=0)
            self.data[name].norm[store] += norm

        return self


if __name__ == "__main__":
    pass
