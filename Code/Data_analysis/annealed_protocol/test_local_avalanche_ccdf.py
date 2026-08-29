import unittest
from collections import Counter

import numpy as np

from local_avalanche_ccdf import empirical_ccdf


class LocalAvalancheCcdfTest(unittest.TestCase):
    def test_empirical_ccdf_uses_exact_unbinned_counts(self):
        sizes, survival = empirical_ccdf(Counter({1: 2, 2: 1, 5: 1}))
        np.testing.assert_array_equal(sizes, np.array([1, 2, 5]))
        np.testing.assert_allclose(survival, np.array([1.0, 0.5, 0.25]))


if __name__ == "__main__":
    unittest.main()
