from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from Code.Data_analysis.reproduce_figure_8 import analyze_ts, parse_fibril_file


class Figure8ReproductionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_raw(self, body: str) -> Path:
        path = self.root / "ts_8_seed_1_m_2.txt"
        path.write_text(
            "f,num_active_particles,num_deleted_particles,total_deleted_rods,"
            "avalanche_sizes\n"
            + body,
            encoding="utf-8",
        )
        return path

    def test_parser_separates_runs_and_cluster_mass(self) -> None:
        source = self.write_raw(
            '0,10,0,0,"0"\n'
            '1,9,1,1,"1"\n'
            '2,0,10,5,"3-1-1"\n'
            '----------------------------------------------1\n'
            '0,12,0,0,"0"\n'
            '4,0,12,4,"4"\n'
        )

        events = parse_fibril_file(source)

        self.assertEqual(events.run_count, 2)
        np.testing.assert_array_equal(events.run_id, [0, 0, 1])
        np.testing.assert_array_equal(events.singleton_mass, [1, 2, 0])
        np.testing.assert_array_equal(events.collective_mass, [0, 3, 4])
        np.testing.assert_allclose(events.terminal_forces, [2.0, 4.0])

    def test_old_file_level_binning_remains_available(self) -> None:
        self.write_raw(
            '0,10,0,0,"0"\n'
            '1,9,1,1,"1"\n'
            '2,0,10,2,"2"\n'
            '----------------------------------------------1\n'
            '0,12,0,0,"0"\n'
            '2,10,2,1,"1"\n'
            '4,0,12,4,"4"\n'
        )

        curve = analyze_ts(self.root, ts=8, bins=2, normalization="file")

        # The file maximum is F=4, so both F=2 rows fall in the first bin.
        # Run 0 has Psi=2/(1+2), while run 1 has Psi=0 in that bin.
        np.testing.assert_allclose(
            curve.mean_collective_fraction, [1.0 / 3.0, 1.0]
        )
        np.testing.assert_array_equal(curve.active_pairs, [2, 1])
        self.assertEqual(curve.file_count, 1)
        self.assertEqual(curve.run_count, 2)

    def test_analysis_defaults_to_realization_normalization(self) -> None:
        self.write_raw(
            '0,10,0,0,"0"\n'
            '1,9,1,1,"1"\n'
            '2,0,10,2,"2"\n'
            '----------------------------------------------1\n'
            '0,12,0,0,"0"\n'
            '2,10,2,1,"1"\n'
            '4,0,12,4,"4"\n'
        )

        curve = analyze_ts(self.root, ts=8, bins=2)

        np.testing.assert_allclose(curve.mean_collective_fraction, [0.0, 1.0])
        np.testing.assert_array_equal(curve.active_pairs, [2, 2])


if __name__ == "__main__":
    unittest.main()
