import tempfile
import unittest
from pathlib import Path

from prepare_local_avalanche_sizes import extract_ts


class PrepareLocalAvalancheSizesTest(unittest.TestCase):
    def test_expands_local_sizes_and_retains_singletons(self):
        fixture = (
            "f,num_active_particles,num_deleted_particles,total_deleted_rods,avalanche_sizes\n"
            '0,10,0,0,"0"\n'
            '0.5,8,2,45,"44-1"\n'
            "----------------------------------------------1\n"
            '0,10,0,5,"3-2"\n'
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ts_dir = root / "runs" / "ts_8"
            output_dir = root / "prepared"
            ts_dir.mkdir(parents=True)
            output_dir.mkdir()
            (ts_dir / "ts_8_seed_130_m_2.txt").write_text(fixture, encoding="utf-8")

            result = extract_ts(ts_dir, output_dir)

            self.assertEqual(
                (output_dir / "ts_8.txt").read_text().splitlines(),
                ["44", "1", "3", "2"],
            )
            self.assertEqual(result["local_events_s_ge_1"], 4)
            self.assertEqual(result["singleton_events_s_eq_1"], 1)
            self.assertEqual(result["analysis_events_s_ge_2"], 3)
            self.assertEqual(result["runs"], 2)
            self.assertEqual(result["max_local_size"], 44)


if __name__ == "__main__":
    unittest.main()
