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


class SigmaTracksCurrentCrossSectionTest(unittest.TestCase):
    """sigma(i)=F/N(i) must follow the CURRENT occupancies (Eqs. 2-3).

    A rod loses cross-sectional area whenever any molecule sharing one of its
    layers is removed.  Before this was fixed, sigma_mean was only recomputed
    when the rod's own neighbourhood changed, so removing a non-neighbour from
    the same layer left a stale, systematically low stress.
    """

    def coplanar_fibril(self, temporary_directory):
        source = Path(temporary_directory) / "fibril.dat"
        # All four rods occupy layers y=0 and y=1.  Rods 1 and 2 are laterally
        # adjacent (|dx|=1), as are rods 3 and 4, but no rod of the first pair
        # neighbours a rod of the second (|dx|>=4).  Removing rod 3 therefore
        # shrinks the cross-sections carrying rod 1 WITHOUT touching rod 1's
        # own neighbourhood -- the case the old cache missed.
        source.write_text(
            "id uid x y z\n"
            "uid 1 0 0 0\n"
            "uid 1 0 1 0\n"
            "uid 2 1 0 0\n"
            "uid 2 1 1 0\n"
            "uid 3 5 0 0\n"
            "uid 3 5 1 0\n"
            "uid 4 6 0 0\n"
            "uid 4 6 1 0\n",
            encoding="utf-8",
        )
        return stress_strain_ava.read_or_create_ssd(str(source))

    @staticmethod
    def exact_sigma(ssd, rod, force):
        per_layer = [
            force / ssd.layers[ssd.particles[pid].lid].len()
            for pid in rod.pids
            if ssd.layers[ssd.particles[pid].lid].len() > 0
        ]
        return sum(per_layer) / len(per_layer)

    def test_removing_a_non_neighbour_in_the_same_layer_raises_sigma(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            ssd = self.coplanar_fibril(temporary_directory)
            force = 10.0
            rod = ssd.rods[1]

            rod.prob_break(force)
            before = rod.sigma_mean
            self.assertAlmostEqual(before, self.exact_sigma(ssd, rod, force))

            # rod 1 is coordinated (N>0) but rod 3 is not among its neighbours,
            # so removing rod 3 never cleared the old `updated` flag
            neighbour_rids = {ssd.particles[pid].rid for pid in rod.neigh_pids}
            self.assertGreater(rod.N, 0)
            self.assertNotIn(3, neighbour_rids)

            ssd.drop_rids({3})
            rod.prob_break(force)

            self.assertAlmostEqual(
                rod.sigma_mean, self.exact_sigma(ssd, rod, force)
            )
            self.assertGreater(rod.sigma_mean, before)

    def test_sigma_scales_linearly_with_force(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            ssd = self.coplanar_fibril(temporary_directory)
            rod = ssd.rods[1]
            rod.prob_break(3.0)
            at_three = rod.sigma_mean
            rod.prob_break(6.0)
            self.assertAlmostEqual(rod.sigma_mean, 2.0 * at_three)


if __name__ == "__main__":
    unittest.main()
