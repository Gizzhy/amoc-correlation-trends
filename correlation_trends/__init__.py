"""Answer key for the correlation-and-trends assignment (Lecture 4).

Worked helpers (``autocorr``, ``integral_timescale``, ``effective_dof``, and the
``data_io`` loader) are provided so students focus on the two estimators left as
stubs in the student version: ``cross_correlation`` and ``trend_with_significance``.
The accompanying ``pytest`` checks encode the behaviour they must satisfy.
"""

from .correlation import (
    autocorr,
    cross_correlation,
    effective_dof,
    integral_timescale,
)
from .data_io import load_47n, load_amoc, load_moc_sigma0_26n, load_ts_gridded
from .geostrophy import (
    dynamic_height,
    interior_geostrophic_transport,
    to_teos10,
)
from .seasonal import remove_seasonal_cycle, seasonal_climatology
from .trends import TrendResult, fit_trend, trend_with_significance

__all__ = [
    "TrendResult",
    "autocorr",
    "cross_correlation",
    "dynamic_height",
    "effective_dof",
    "fit_trend",
    "integral_timescale",
    "interior_geostrophic_transport",
    "load_47n",
    "load_amoc",
    "load_moc_sigma0_26n",
    "load_ts_gridded",
    "remove_seasonal_cycle",
    "seasonal_climatology",
    "to_teos10",
    "trend_with_significance",
]
