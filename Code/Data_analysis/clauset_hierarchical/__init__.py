"""Block-aware Clauset analysis for local preterminal avalanches."""

from .diagnostics import leave_one_fibril_out, subset_stability, weighted_quantile

__all__ = ["leave_one_fibril_out", "subset_stability", "weighted_quantile"]

from .analysis import (
    BlockPowerLawResult,
    BlockModelGoodnessOfFit,
    FibrilHistograms,
    ModelComparison,
    fit_block_power_law,
    fit_block_model_gof,
    fit_competing_models,
    load_fibril_histograms,
)

__all__ = [
    "BlockPowerLawResult",
    "BlockModelGoodnessOfFit",
    "FibrilHistograms",
    "ModelComparison",
    "fit_block_power_law",
    "fit_block_model_gof",
    "fit_competing_models",
    "load_fibril_histograms",
]
