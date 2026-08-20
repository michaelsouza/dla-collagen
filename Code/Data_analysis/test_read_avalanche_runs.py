import csv
import io
import tempfile
import unittest
from pathlib import Path

import duckdb
import read_avalanche_runs as reader


HEADER = (
    "f,num_active_particles,num_deleted_particles,total_deleted_rods,"
    "avalanche_sizes\n"
)


class AvalancheRunReaderTest(unittest.TestCase):
    def make_run_file(self, root: Path, body: str, *, ts: int = 2) -> Path:
        directory = root / f"ts_{ts}"
        directory.mkdir(parents=True)
        path = directory / f"ts_{ts}_seed_130_m_2.txt"
        path.write_text(HEADER + body, encoding="utf-8")
        return path

    def test_reads_realizations_and_preserves_all_cluster_sizes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = self.make_run_file(
                Path(temporary_directory),
                '0,18,0,0,"0"\n'
                '0.5,9,9,3,"2-1"\n'
                '1.0,0,18,4,"4"\n'
                '----------------------------------------------1\n'
                '0,18,0,0,"0"\n'
                '0.5,0,18,5,"3-2"\n',
            )

            steps = list(reader.iter_force_steps(path))
            self.assertEqual([step.realization for step in steps], [0, 0, 0, 1, 1])
            self.assertEqual(steps[1].avalanche_sizes, (2, 1))
            self.assertTrue(steps[-1].is_terminal)

            events = list(
                reader.iter_avalanche_events(steps, minimum_size=2)
            )
            self.assertEqual([event.size for event in events], [2, 4, 3, 2])
            self.assertEqual([event.realization for event in events], [0, 0, 1, 1])

    def test_reads_numbered_separators_from_crlf_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            directory = root / "ts_16"
            directory.mkdir()
            path = directory / "ts_16_seed_1630_m_2.txt"
            path.write_bytes(
                (
                    HEADER
                    + '0,18,0,0,"0"\n'
                    + '0.5,0,18,1,"1"\n'
                    + '----------------------------------------------1\n'
                    + '0,18,0,0,"0"\n'
                    + '0.5,0,18,2,"2"\n'
                ).replace("\n", "\r\n").encode("ascii")
            )

            steps = list(reader.iter_force_steps(path))

            self.assertEqual([step.realization for step in steps], [0, 0, 1, 1])
            self.assertEqual(steps[-1].avalanche_sizes, (2,))

    def test_cli_uses_complete_fibril_dataset_by_default(self):
        args = reader.build_argument_parser().parse_args(["summary"])
        self.assertEqual(args.root, reader.DEFAULT_RUN_ROOT)

    def test_reports_cluster_total_mismatch_with_line_number(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = self.make_run_file(
                Path(temporary_directory),
                '0,18,0,0,"0"\n'
                '0.5,0,18,4,"2-1"\n',
            )

            with self.assertRaisesRegex(
                reader.RunDataError,
                r":3: sum\(avalanche_sizes\).*3 != 4",
            ):
                list(reader.iter_force_steps(path))

    def test_reports_nonterminal_realization(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = self.make_run_file(
                Path(temporary_directory),
                '0,18,0,0,"0"\n'
                '0.5,9,9,1,"1"\n',
            )

            with self.assertRaisesRegex(
                reader.RunDataError,
                "realization 0 has no terminal row",
            ):
                list(reader.iter_force_steps(path))

    def test_discovers_files_in_numeric_condition_order(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for ts in (128, 2, 16):
                self.make_run_file(root, '0,18,0,0,"0"\n0.5,0,18,1,"1"\n', ts=ts)

            run_files = reader.discover_run_files(root)
            self.assertEqual([run_file.ts for run_file in run_files], [2, 16, 128])
            self.assertEqual(
                [run_file.fibril_id for run_file in run_files],
                ["ts_2_seed_130", "ts_16_seed_130", "ts_128_seed_130"],
            )

    def test_summary_tracks_hierarchy_and_selection(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = self.make_run_file(
                Path(temporary_directory),
                '0,18,0,0,"0"\n'
                '0.5,9,9,3,"2-1"\n'
                '1.0,0,18,4,"4"\n'
                '----------------------------------------------1\n'
                '0,18,0,0,"0"\n'
                '0.5,0,18,1,"1"\n',
            )

            summary = reader.summarize_dataset(
                [reader.parse_run_file(path)],
                minimum_size=2,
                include_terminal_step=False,
            )

            self.assertEqual(summary["totals"]["files"], 1)
            self.assertEqual(summary["totals"]["realizations"], 2)
            self.assertEqual(summary["totals"]["events_all_sizes"], 4)
            self.assertEqual(summary["totals"]["singleton_events"], 2)
            self.assertEqual(summary["totals"]["selected_events"], 1)

    def test_csv_export_contains_fibril_and_source_provenance(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = self.make_run_file(
                Path(temporary_directory),
                '0,18,0,0,"0"\n0.5,0,18,3,"2-1"\n',
            )
            output = io.StringIO()

            count = reader.write_events_csv(
                [reader.parse_run_file(path)],
                output,
                minimum_size=2,
            )
            rows = list(csv.DictReader(io.StringIO(output.getvalue())))

            self.assertEqual(count, 1)
            self.assertEqual(rows[0]["fibril_id"], "ts_2_seed_130")
            self.assertEqual(rows[0]["realization"], "0")
            self.assertEqual(rows[0]["step_index"], "1")
            self.assertEqual(rows[0]["avalanche_size"], "2")
            self.assertEqual(rows[0]["source_line"], "3")

    def test_parquet_cache_preserves_raw_events_and_is_queryable(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = self.make_run_file(
                root,
                '0,18,0,0,"0"\n'
                '0.5,9,9,3,"2-1"\n'
                '1.0,0,18,4,"4"\n'
                '----------------------------------------------1\n'
                '0,18,0,0,"0"\n'
                '0.5,0,18,1,"1"\n',
            )
            output = root / "derived" / "rupture-v1"
            counts = reader.build_parquet_cache(
                [reader.parse_run_file(path)], output, root=root, workers=2
            )

            self.assertEqual(counts["files"], 1)
            self.assertEqual(counts["realizations"], 2)
            self.assertEqual(counts["avalanche_events"], 4)
            connection = duckdb.connect()
            events_glob = (output / "avalanche_events" / "**" / "*.parquet").as_posix()
            rows = connection.execute(
                "SELECT avalanche_size, is_terminal_step, ts, weibull_modulus "
                "FROM read_parquet(?, hive_partitioning=true) "
                "ORDER BY realization, step_index, event_index",
                [events_glob],
            ).fetchall()
            self.assertEqual(rows, [(2, False, 2, 2), (1, False, 2, 2),
                                    (4, True, 2, 2), (1, True, 2, 2)])
            manifest = connection.execute(
                "SELECT schema_version, source_sha256, realizations "
                "FROM read_parquet(?)",
                [(output / "manifest" / "manifest.parquet").as_posix()],
            ).fetchone()
            self.assertEqual(manifest[0], reader.SCHEMA_VERSION)
            self.assertEqual(len(manifest[1]), 64)
            self.assertEqual(manifest[2], 2)
            connection.close()

            histogram_glob = (
                output / "run_histograms" / "**" / "*.parquet"
            ).as_posix()
            connection = duckdb.connect()
            histogram = connection.execute(
                "SELECT realization, is_terminal_step, avalanche_size, event_count "
                "FROM read_parquet(?, hive_partitioning=true) "
                "ORDER BY ALL",
                [histogram_glob],
            ).fetchall()
            self.assertEqual(
                histogram,
                [(0, False, 1, 1), (0, False, 2, 1),
                 (0, True, 4, 1), (1, True, 1, 1)],
            )
            connection.close()

    def test_analysis_database_preserves_hierarchy_and_event_totals(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = self.make_run_file(
                root,
                '0,18,0,0,"0"\n'
                '0.5,9,9,3,"2-1"\n'
                '1.0,0,18,4,"4"\n'
                '----------------------------------------------1\n'
                '0,18,0,0,"0"\n'
                '0.5,0,18,1,"1"\n',
            )
            cache = root / "derived" / "rupture-v1"
            database = root / "derived" / "analysis.duckdb"
            reader.build_parquet_cache(
                [reader.parse_run_file(path)], cache, root=root
            )

            counts = reader.build_analysis_database(cache, database)

            self.assertEqual(counts["run_summary"], 2)
            self.assertEqual(counts["avalanche_events_represented"], 4)
            connection = duckdb.connect(database.as_posix(), read_only=True)
            pooled = connection.execute(
                "SELECT is_terminal_step, avalanche_size, event_count "
                "FROM pooled_histograms ORDER BY ALL"
            ).fetchall()
            self.assertEqual(
                pooled,
                [(False, 1, 1), (False, 2, 1),
                 (True, 1, 1), (True, 4, 1)],
            )
            self.assertEqual(
                connection.execute("SELECT count(*) FROM avalanche_events").fetchone()[0],
                4,
            )
            connection.close()

    def test_cache_refuses_to_overwrite_existing_output(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = self.make_run_file(
                root, '0,18,0,0,"0"\n0.5,0,18,1,"1"\n'
            )
            output = root / "existing"
            output.mkdir()
            with self.assertRaisesRegex(reader.RunDataError, "already exists"):
                reader.build_parquet_cache(
                    [reader.parse_run_file(path)], output, root=root
                )


if __name__ == "__main__":
    unittest.main()
