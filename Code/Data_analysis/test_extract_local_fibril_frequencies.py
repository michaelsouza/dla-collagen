import tempfile
import unittest
from pathlib import Path

from extract_local_fibril_frequencies import extract_file


class ExtractFibrilFrequenciesTest(unittest.TestCase):
    def test_extracts_non_singletons_and_includes_terminal(self):
        fixture = (
            "f,num_active_particles,num_deleted_particles,total_deleted_rods,avalanche_sizes\n"
            '0,10,0,0,"0"\n0.5,8,2,3,"2-1"\n1,0,10,4,"4"\n'
            "----------------------------------------------1\n"
            '0,10,0,0,"0"\n0.5,7,3,3,"3"\n1,0,10,4,"4"\n'
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ts_8_seed_130_m_2.txt"
            path.write_text(fixture, encoding="utf-8")
            rows = extract_file(path)
        self.assertEqual(
            [(row["local_size"], row["frequency"]) for row in rows],
            [(2, 1), (3, 1), (4, 2)],
        )
        self.assertTrue(all(row["runs"] == 2 for row in rows))


if __name__ == "__main__":
    unittest.main()
