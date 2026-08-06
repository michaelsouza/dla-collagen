import unittest
from collections import Counter

import numpy as np

from plot_local_avalanche_filtered import binned_density


class BinnedDensityTest(unittest.TestCase):
    def test_counts_are_conserved_and_density_is_width_corrected(self):
        centers, density, counts = binned_density(Counter({2: 4, 3: 2, 5: 6}), np.array([2, 4, 8]))
        np.testing.assert_array_equal(counts, np.array([6, 6]))
        self.assertEqual(counts.sum(), 12)
        self.assertAlmostEqual(float(np.sum(density * np.array([2, 4]))), 1.0)
        self.assertEqual(len(centers), 2)


if __name__ == "__main__":
    unittest.main()
