import tempfile
import unittest
from pathlib import Path

from local_avalanche_counts import aggregate_by_ts, parse_local_sizes, summarize_file


class LocalAvalancheCountsTest(unittest.TestCase):
    def test_parse_local_sizes(self):
        self.assertEqual(parse_local_sizes('"3-1-1"'), (3, 1, 1))
        self.assertEqual(parse_local_sizes('"0"'), ())

    def test_summarize_file_preserves_runs_and_terminal_partition(self):
        content = """f,num_active_particles,num_deleted_particles,total_deleted_rods,avalanche_sizes
0,10,0,0,"0"
1,8,2,2,"1-1"
2,0,10,3,"3"
----------------------------------------------1
0,12,0,0,"0"
1,9,3,3,"2-1"
2,0,12,4,"4"
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ts_8_seed_1000_m_2.txt"
            path.write_text(content, encoding="utf-8")
            row = summarize_file(path)

        self.assertEqual(row["runs"], 2)
        self.assertEqual(row["terminal_runs"], 2)
        self.assertEqual(row["local_events"], 6)
        self.assertEqual(row["preterminal_events"], 4)
        self.assertEqual(row["terminal_events"], 2)
        self.assertEqual(row["singleton_events"], 3)
        self.assertEqual(row["max_local_size"], 4)

    def test_aggregate_by_ts_sums_counts_and_takes_maximum(self):
        row = {
            "ts": 2,
            "fibril_seed": 1,
            "weibull_m": 2,
            "runs": 2,
            "terminal_runs": 2,
            "force_steps": 5,
            "nonzero_force_steps": 3,
            "local_events": 4,
            "preterminal_events": 2,
            "terminal_events": 2,
            "rods_in_local_events": 8,
            "preterminal_rods": 3,
            "terminal_rods": 5,
            "singleton_events": 1,
            "max_local_size": 5,
        }
        other = dict(row, fibril_seed=2, max_local_size=7)
        summary = aggregate_by_ts([row, other])[0]
        self.assertEqual(summary["fibrils"], 2)
        self.assertEqual(summary["local_events"], 8)
        self.assertEqual(summary["max_local_size"], 7)


if __name__ == "__main__":
    unittest.main()
