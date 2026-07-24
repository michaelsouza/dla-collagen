import tempfile
import unittest
from pathlib import Path

import extend_fibrils_batch


class ExtendedFilenameTest(unittest.TestCase):
    def test_extracts_ts_and_seed(self):
        source_name = "dla_mode_s_ts_512_nb_30000_seed_4135_.dat"
        self.assertEqual(
            extend_fibrils_batch.extended_filename(source_name),
            "ts_512_seed_4135.dat",
        )

    def test_rejects_unrecognized_name(self):
        with self.assertRaises(ValueError):
            extend_fibrils_batch.extended_filename("fibril.dat")


class ExtendFibrilTest(unittest.TestCase):
    def test_expands_each_molecule_along_y(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "compact.dat"
            destination = root / "extended.dat"
            source.write_text(
                "metadata ignored\n"
                "uid: 7 2 -1 4\n"
                "uid: 8 3 5 6\n",
                encoding="utf-8",
            )

            result = extend_fibrils_batch.extend_fibril(
                source,
                destination,
                rod_length=3,
            )

            self.assertEqual(result.molecules, 2)
            self.assertEqual(result.occupied_sites, 6)
            self.assertEqual(
                destination.read_text(encoding="utf-8").splitlines(),
                [
                    "id uid x y z",
                    "uid 7 2 -1 4",
                    "uid 7 2 0 4",
                    "uid 7 2 1 4",
                    "uid 8 3 5 6",
                    "uid 8 3 6 6",
                    "uid 8 3 7 6",
                ],
            )

    def test_does_not_overwrite_by_default(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "compact.dat"
            destination = root / "extended.dat"
            source.write_text("uid: 1 0 0 0\n", encoding="utf-8")
            destination.write_text("keep me\n", encoding="utf-8")

            result = extend_fibrils_batch.extend_fibril(source, destination)

            self.assertEqual(result.status, "skipped")
            self.assertEqual(destination.read_text(encoding="utf-8"), "keep me\n")


if __name__ == "__main__":
    unittest.main()
