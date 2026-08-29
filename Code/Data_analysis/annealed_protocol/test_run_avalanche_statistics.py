import hashlib
import tempfile
import unittest
from pathlib import Path

from Code.Data_analysis.avalanche_statistics import avalanche_parser_signature
from Code.Data_analysis.run_avalanche_statistics import (
    MANIFEST_SCHEMA_VERSION,
    _merge_manifest_data,
    _migrate_legacy_manifest,
)


class CacheProvenanceTest(unittest.TestCase):
    def test_parser_signature_is_a_sha256_digest(self):
        signature = avalanche_parser_signature()

        self.assertEqual(len(signature), 64)
        int(signature, 16)
        self.assertEqual(signature, avalanche_parser_signature())


class StagedManifestTest(unittest.TestCase):
    def test_legacy_gof_is_migrated_with_code_and_artifact_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            inventory = output / "inventory.csv"
            fits = output / "observed_model_fits.csv"
            gof = output / "power_law_gof.csv"
            replicas = output / "power_law_gof_replicates.csv"
            for path, contents in (
                (inventory, "inventory\n"),
                (fits, "fits\n"),
                (gof, "gof\n"),
                (replicas, "replicas\n"),
            ):
                path.write_text(contents, encoding="utf-8")

            legacy = {
                "created_utc": "2026-07-31T23:03:30+00:00",
                "analysis_scope": {
                    "ts": [2, 8, 32],
                    "clauset_gof_replicates": 2500,
                    "hierarchical_bootstrap_replicates": 0,
                    "cutoff_likelihood_ratio_bootstrap_replicates": 0,
                    "bootstrap_master_seed": 12738,
                },
                "software": {"python": "3.13.9"},
                "analysis_files": {
                    "module": {"sha256": "old-module"},
                    "runner": {"sha256": "old-runner"},
                },
                "sources": [{"path": "raw.txt", "sha256": "raw-hash"}],
            }

            migrated = _migrate_legacy_manifest(legacy, output)

        self.assertEqual(migrated["manifest_schema_version"], MANIFEST_SCHEMA_VERSION)
        self.assertIn("observed", migrated["stages"])
        self.assertIn("power_law_gof:power_law_gof", migrated["stages"])
        stage = migrated["stages"]["power_law_gof:power_law_gof"]
        self.assertEqual(stage["analysis_files"]["runner"]["sha256"], "old-runner")
        self.assertEqual(stage["scope"]["replicates"], 2500)
        artifact = next(item for item in stage["artifacts"] if item["path"] == gof.name)
        self.assertEqual(
            artifact["sha256"], hashlib.sha256(b"gof\n").hexdigest()
        )

    def test_merging_a_new_stage_preserves_the_completed_gof_stage(self):
        existing = {
            "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
            "stages": {"power_law_gof:power_law_gof": {"marker": "preserve"}},
            "invocations": [{"id": "first"}],
        }
        merged = _merge_manifest_data(
            existing,
            stage_updates={"hierarchical_bootstrap": {"marker": "new"}},
            invocation={"id": "second"},
        )

        self.assertEqual(
            merged["stages"]["power_law_gof:power_law_gof"]["marker"],
            "preserve",
        )
        self.assertEqual(merged["stages"]["hierarchical_bootstrap"]["marker"], "new")
        self.assertEqual([item["id"] for item in merged["invocations"]], ["first", "second"])


if __name__ == "__main__":
    unittest.main()
