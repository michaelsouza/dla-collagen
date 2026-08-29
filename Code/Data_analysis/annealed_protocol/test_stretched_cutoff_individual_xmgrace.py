from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from clauset_hierarchical.analysis import (
    BlockModelBootstrapFit,
    BlockModelGoodnessOfFit,
    FibrilHistograms,
)
from clauset_pooled.models import ModelFit
from run_stretched_cutoff_individual import (
    MODELS,
    ConditionResult,
    write_xmgrace_ccdfs,
    write_xmgrace_model_gof,
    write_xmgrace_parameter,
    write_pooled_counts,
)


class XmgraceExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.fit = ModelFit(
            model="stretched_cutoff_power_law",
            xmin=2,
            parameters={"alpha": 2.0, "beta": 1.5, "scale": 8.0},
            log_likelihood=-10.0,
            ks=0.02,
            n_tail=6,
            parameter_count=3,
        )
        goodness = []
        for index, model in enumerate(MODELS):
            bootstrap = tuple(
                BlockModelBootstrapFit(
                    replicate=replicate,
                    ks=0.03,
                    centered_ks=0.01,
                    parameters={
                        "alpha": 1.8 + 0.4 * replicate,
                        "beta": 1.3 + 0.4 * replicate,
                        "scale": 7.0 + 2.0 * replicate,
                    },
                )
                for replicate in range(2)
            )
            goodness.append(BlockModelGoodnessOfFit(
                model=model,
                xmin=2,
                ks=0.02,
                p_value=0.1 * (index + 1),
                exceedances=index + 1,
                replicates=10,
                centered_ks=(0.01,),
                bootstrap=bootstrap,
            ))
        self.result = ConditionResult(
            ts=8,
            total_events=7,
            maximum_size=4,
            selected=self.fit,
            xmin_candidates=(self.fit,),
            fits=(self.fit,),
            goodness=tuple(goodness),
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_ccdf_sets_alternate_empirical_and_model(self) -> None:
        data = FibrilHistograms(
            ts=8,
            seeds=np.array([1]),
            counts=np.array([[0, 1, 3, 2, 1]], dtype=np.int64),
        )
        path = self.root / "ccdf.dat"
        with mock.patch(
            "run_stretched_cutoff_individual.load_fibril_histograms",
            return_value=data,
        ):
            manifest = write_xmgrace_ccdfs(
                Path("unused.duckdb"), [self.result], path
            )

        text = path.read_text(encoding="utf-8")
        self.assertIn("# S0: Ts=8; empirical; xmin=2", text)
        self.assertIn("# S1: Ts=8; model; xmin=2", text)
        self.assertEqual(text.count("\n&\n"), 1)
        self.assertEqual([row["content"] for row in manifest], ["empirical", "model"])

    def test_parameter_file_declares_asymmetric_errors(self) -> None:
        path = self.root / "alpha.dat"
        write_xmgrace_parameter([self.result], "alpha", path)
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "@type xydydy")
        values = [float(value) for value in lines[-1].split()]
        self.assertEqual(values[:2], [8.0, 2.0])
        self.assertGreater(values[2], 0.0)
        self.assertGreater(values[3], 0.0)

    def test_gof_file_has_one_set_per_model(self) -> None:
        path = self.root / "gof.dat"
        manifest = write_xmgrace_model_gof([self.result], path)
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count("\n&\n"), len(MODELS) - 1)
        self.assertEqual(len(manifest), len(MODELS))

    def test_pooled_counts_include_body_and_normalized_probability(self) -> None:
        data = FibrilHistograms(
            ts=8,
            seeds=np.array([1]),
            counts=np.array([[0, 1, 3, 0, 2]], dtype=np.int64),
        )
        with mock.patch(
            "run_stretched_cutoff_individual.load_fibril_histograms",
            return_value=data,
        ):
            write_pooled_counts(Path("unused.duckdb"), [self.result], self.root)

        lines = (self.root / "pooled_counts_Ts_8.dat").read_text(
            encoding="utf-8"
        ).splitlines()
        self.assertIn("# total_events = 6", lines)
        rows = [
            [float(value) for value in line.split()]
            for line in lines
            if line[0].isdigit()
        ]
        self.assertEqual([int(row[0]) for row in rows], [1, 2, 4])
        self.assertEqual([int(row[1]) for row in rows], [1, 3, 2])
        self.assertAlmostEqual(sum(row[2] for row in rows), 1.0)


if __name__ == "__main__":
    unittest.main()
