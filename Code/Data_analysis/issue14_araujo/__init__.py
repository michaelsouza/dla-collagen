"""Independent validation tools for revision Issue 14.

This package intentionally does not import the exploratory avalanche-fitting
scripts or the Issue 5 implementation.  It works from integer histograms and
the supplied PMFs so that the statistical implementation can be tested in
isolation.
"""

from .models import FitResult, fit_model

__all__ = ["FitResult", "fit_model"]
