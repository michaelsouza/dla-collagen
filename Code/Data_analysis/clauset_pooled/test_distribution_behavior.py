import unittest

import numpy as np

from .distribution_behavior import (
    ccdf_crossings,
    characteristic_size,
    lorenz_curve,
    normalized_quantile_distance,
    split_two_scales,
    top_event_damage_share,
)


class DistributionBehaviorTest(unittest.TestCase):
    def test_characteristic_size_and_top_share(self):
        histogram = np.array([0, 0, 2, 0, 2], dtype=np.int64)
        self.assertAlmostEqual(characteristic_size(histogram), 10.0 / 3.0)
        actual_fraction, size_share = top_event_damage_share(histogram, 0.5)
        self.assertEqual(actual_fraction, 0.5)
        self.assertAlmostEqual(size_share, 2.0 / 3.0)

    def test_lorenz_curve_has_correct_endpoints(self):
        histogram = np.array([0, 0, 2, 0, 2], dtype=np.int64)
        events, sizes = lorenz_curve(histogram, points=11)
        self.assertEqual(events[0], 0.0)
        self.assertEqual(events[-1], 1.0)
        self.assertEqual(sizes[0], 0.0)
        self.assertEqual(sizes[-1], 1.0)
        self.assertTrue(np.all(np.diff(sizes) >= 0.0))

    def test_two_scale_split_finds_separated_groups(self):
        histogram = np.zeros(110, dtype=np.int64)
        histogram[2:5] = (500, 300, 200)
        histogram[95:106] = 20
        result = split_two_scales(histogram)
        self.assertEqual(result.small_maximum, 4)
        self.assertEqual(result.large_minimum, 95)
        self.assertGreater(result.explained_log_variance, 0.9)

    def test_ccdf_crossing_is_detected(self):
        first = np.array([0, 0, 80, 0, 0, 20], dtype=np.int64)
        second = np.array([0, 0, 90, 0, 0, 10], dtype=np.int64)
        crossings = ccdf_crossings(first, second, minimum_difference=0.0)
        self.assertTrue(crossings)

    def test_normalized_quantile_distance_vanishes_for_scaled_shape(self):
        first = np.zeros(21, dtype=np.int64)
        second = np.zeros(41, dtype=np.int64)
        first[[2, 4, 8, 16]] = 100
        second[[4, 8, 16, 32]] = 100
        distance = normalized_quantile_distance(
            first, second, first_minimum=2, second_minimum=4
        )
        self.assertAlmostEqual(distance, 0.0)


if __name__ == "__main__":
    unittest.main()

