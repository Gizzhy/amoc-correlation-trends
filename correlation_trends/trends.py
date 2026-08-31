"""Linear trends and their significance for autocorrelated series.

Worked helper: :func:`fit_trend`. Student stub: :func:`trend_with_significance`.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
from numpy.typing import ArrayLike
from scipy import stats

from .correlation import effective_dof


class TrendResult(NamedTuple):
    """Result of :func:`trend_with_significance`.

    Attributes
    ----------
    slope, intercept : float
        Least-squares fit coefficients (``x ~ slope * t + intercept``).
    se : float
        Naive OLS standard error of the slope (assumes independent residuals).
    se_eff : float
        Standard error inflated for autocorrelation, ``se * sqrt(N / N_eff)``.
    p_naive, p_eff : float
        Two-sided p-values for ``slope = 0`` using ``se`` (with ``N - 2`` d.o.f.)
        and ``se_eff`` (with ``N_eff - 2`` d.o.f.) respectively.
    n_eff : float
        Effective sample size ``N / (1 + 2 sum rho_k)`` from the residuals.
    t_naive, t_eff : float
        Slope in units of its standard error (``slope / se`` and ``slope / se_eff``)
        -- how many sigma the slope sits from zero. Significant at 95% needs
        ``|t| > ~1.96``.
    """

    slope: float
    intercept: float
    se: float
    se_eff: float
    p_naive: float
    p_eff: float
    n_eff: float
    t_naive: float
    t_eff: float


def fit_trend(t: ArrayLike, x: ArrayLike) -> tuple[float, float]:
    """Least-squares straight-line fit.

    Parameters
    ----------
    t : array_like
        Predictor (e.g. time).
    x : array_like
        Response series.

    Returns
    -------
    slope, intercept : float
        Coefficients of ``x ~ slope * t + intercept``.
    """
    slope, intercept = np.polyfit(np.asarray(t, float), np.asarray(x, float), 1)
    return float(slope), float(intercept)


def trend_with_significance(t: ArrayLike, x: ArrayLike, dt: float) -> TrendResult:
    t = np.asarray(t, dtype=float)
    x = np.asarray(x, dtype=float)
    n = t.size
    slope, intercept = fit_trend(t, x)
    resid = x - (slope * t + intercept)
    ss_t = np.sum((t - t.mean()) ** 2)
    sigma2 = np.sum(resid ** 2) / (n - 2)
    se = np.sqrt(sigma2 / ss_t)
    n_eff = effective_dof(resid, dt)
    se_eff = se * np.sqrt(n / n_eff)
    t_naive = slope / se
    t_eff = slope / se_eff
    p_naive = 2.0 * stats.t.sf(abs(t_naive), n - 2)
    p_eff = 2.0 * stats.t.sf(abs(t_eff), max(n_eff - 2.0, 1.0))
    return TrendResult(
        slope=float(slope), intercept=float(intercept), se=float(se),
        se_eff=float(se_eff), p_naive=float(p_naive), p_eff=float(p_eff),
        n_eff=float(n_eff), t_naive=float(t_naive), t_eff=float(t_eff),
    )
