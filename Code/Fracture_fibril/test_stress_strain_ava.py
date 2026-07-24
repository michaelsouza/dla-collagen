import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import stress_strain_ava


class FakeStressStrainData:
    """Minimal state needed to exercise the force-step rupture loop."""

    def __init__(self, rods=None):
        self.rods = dict(
            {1: object(), 2: object(), 3: object()} if rods is None else rods
        )
        self.last_drop = set()

    def copy(self):
        snapshot = FakeStressStrainData(self.rods)
        snapshot.last_drop = self.last_drop.copy()
        return snapshot

    def num_active_particles(self):
        return len(self.rods)

    def drop_rids(self, to_drop):
        self.last_drop = set(to_drop)
        for rid in to_drop:
            self.rods.pop(rid, None)

    def filter_rids(self, reverse=True):
        if self.last_drop == {3}:
            return set(), set()
        return set(self.rods), set()


class ForceLevelAvalancheTest(unittest.TestCase):
    def test_adjacent_removals_from_successive_sweeps_are_grouped_at_same_force(self):
        deletion_batches = iter(([1], [2], [], [3]))
        cluster_calls = []

        def deterministic_deletions(_ssd, _force):
            return next(deletion_batches)

        def cluster_size_from_accumulated_ids(snapshot, deleted_rids):
            cluster_calls.append((set(snapshot.rods), set(deleted_rids)))
            return [len(deleted_rids)] if deleted_rids else []

        with (
            patch.object(
                stress_strain_ava,
                "random_deleted_rids",
                side_effect=deterministic_deletions,
            ),
            patch.object(
                stress_strain_ava,
                "find_deleted_rod_clusters",
                side_effect=cluster_size_from_accumulated_ids,
            ),
        ):
            logger = stress_strain_ava.stress_strain(FakeStressStrainData())

        nonempty_clusters_at_first_force = [
            clusters
            for force, clusters in zip(logger.F, logger.deleted_rod_clusters)
            if force == 0.5 and clusters
        ]
        self.assertEqual(nonempty_clusters_at_first_force, [[2]])
        self.assertIn(({1, 2, 3}, {1, 2}), cluster_calls)


class ExtendedDatInputTest(unittest.TestCase):
    def test_ignores_the_extended_file_header(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "fibril.dat"
            source.write_text(
                "id uid x y z\n"
                "uid 7 0 0 0\n"
                "uid 7 0 1 0\n",
                encoding="utf-8",
            )

            ssd = stress_strain_ava.read_or_create_ssd(str(source))

            self.assertEqual(set(ssd.rods), {7})
            self.assertEqual(len(ssd.rods[7].pids), 2)
            self.assertTrue(source.with_suffix(".db").exists())


if __name__ == "__main__":
    unittest.main()
