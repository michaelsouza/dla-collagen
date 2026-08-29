from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from Code.Data_analysis.reproduce_figure_7 import analyze_ts, parse_damage_file


class Figure7ReproductionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_raw(self) -> Path:
        path = self.root / "ts_8_seed_1_m_2.txt"
        path.write_text(
            "f,num_active_particles,num_deleted_particles,total_deleted_rods,"
            "avalanche_sizes\n"
            '0,10,0,0,"0"\n'
            '1,9,1,1,"1"\n'
            '1,8,2,1,"1"\n'
            '2,0,10,8,"8"\n'
            '----------------------------------------------1\n'
            '0,20,0,0,"0"\n'
            '1,18,2,2,"2"\n'
            '2,10,10,8,"8"\n'
            '3,0,20,10,"10"\n',
            encoding="utf-8",
        )
        return path

    def test_parser_keeps_last_preterminal_state_per_force(self) -> None:
        source = self.write_raw()

        damage, runs = parse_damage_file(source)

        self.assertEqual(runs, 2)
        np.testing.assert_allclose(damage[0.0], [0.0, 0.0])
        np.testing.assert_allclose(damage[1.0], [20.0, 10.0])
        np.testing.assert_allclose(damage[2.0], [50.0])
        self.assertNotIn(3.0, damage)

    def test_support_filter_uses_fraction_of_all_runs(self) -> None:
        self.write_raw()

        curve = analyze_ts(self.root, ts=8, minimum_support=0.75)

        np.testing.assert_allclose(curve.force, [0.0, 1.0])
        np.testing.assert_allclose(curve.mean_percent, [0.0, 15.0])
        np.testing.assert_allclose(curve.support_fraction, [1.0, 1.0])
        self.assertEqual(curve.total_realizations, 2)


if __name__ == "__main__":
    unittest.main()
