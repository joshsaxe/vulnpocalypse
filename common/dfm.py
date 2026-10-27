"""A one-factor dynamic model that merges many noisy loss series into one latent trend (Gibbs sampler).

Model, on the log scale, for series s and year t (missing values allowed):
    y[s,t] = alpha[s] + delta[s] * (t - t_center) + x[t] + e[s,t],        e ~ Normal(0, sigma[s]^2)
    x[t] - 2 x[t-1] + x[t-2] ~ Normal(0, tau^2)       (a smooth trend whose growth rate can drift a little each year)
alpha[ref] = 0 pins the level of x to a reference series. Every other series' level (alpha), its slow reporting drift
(delta), its noise (sigma) and the shared trend (x) are learned.
Priors: alpha[s] ~ N(0, 10^2); delta[s] ~ N(0, drift_sd^2); sigma[s]^2 ~ InvGamma(a_s, b_s) (weakly informative, per-series
prior scale); tau^2 ~ InvGamma(2, 0.02) (a growth rate that drifts a few points a year); a very weak ridge on x.
All full conditionals are conjugate, so a Gibbs sampler is exact and fast.
"""
from __future__ import annotations

import numpy as np


def second_diff_matrix(T):
    D = np.zeros((T - 2, T))
    for i in range(T - 2):
        D[i, i:i + 3] = [1.0, -2.0, 1.0]
    return D


def forecast_from(x_draws, t_end, horizon, tau_draws, rng=None):
    """Extend each trend draw past index t_end by `horizon` steps under the smooth-trend prior.

    Used for the counterfactual: fit on years up to t_end (pre-ChatGPT), project the years after it.
    """
    rng = rng or np.random.default_rng(7)
    n = x_draws.shape[0]
    out = np.empty((n, horizon))
    for i in range(n):
        x1, x0 = x_draws[i, t_end], x_draws[i, t_end - 1]
        g = x1 - x0
        cur = x1
        for h in range(horizon):
            g = g + rng.normal(0, tau_draws[i])
            cur = cur + g
            out[i, h] = cur
    return out


def gibbs_dfm_drift(Y, years, ref=0, drift_sd=0.03, n_iter=8000, n_burn=2000, seed=1, sigma_prior=None,
                    tau_prior=(2.0, 0.02), t_center=None, n_chains=1):
    """One-factor model with series-specific linear drift, sampled with a joint Gaussian block.

        y[s,t] = alpha[s] + delta[s] * (t - t_center) + x[t] + e[s,t],   e ~ N(0, sigma[s]^2)
        x[t] - 2x[t-1] + x[t-2] ~ N(0, tau^2);   delta[s] ~ N(0, drift_sd[s]^2);  alpha[ref] = 0

    delta lets each series' reporting rate drift relative to the common trend, so a series that grows faster than
    the others because more victims learn to report to it does not drag the shared trend with it. Because the
    deltas are centred on zero, the shared trend's own slope is the precision-weighted average of the series'
    slopes; any drift common to all series cannot be separated from true growth and is handled outside this
    function (see models/c01_loss_trend.py).

    Conditional on (sigma, tau), (x, alpha, delta) is jointly Gaussian and is drawn in one block, so the sampler
    mixes well even though the trend's slope and the drifts are correlated.
    """
    rng = np.random.default_rng(seed)
    S, T = Y.shape
    years = np.asarray(years, float)
    tc = years[-1] if t_center is None else t_center
    obs = ~np.isnan(Y)
    D = second_diff_matrix(T)
    DtD = D.T @ D
    dsd = np.broadcast_to(np.asarray(drift_sd, float), (S,)).copy()
    if sigma_prior is None:
        sigma_prior = [(3.0, 3.0 * 0.2 ** 2)] * S
    P = T + 2 * S
    # observation design
    rows = []
    for s in range(S):
        for t in np.where(obs[s])[0]:
            a = np.zeros(P)
            a[t] = 1.0
            a[T + s] = 1.0
            a[T + S + s] = years[t] - tc
            rows.append((s, t, a))
    A = np.array([r[2] for r in rows])
    yv = np.array([Y[r[0], r[1]] for r in rows])
    sidx = np.array([r[0] for r in rows])
    # prior precision (fixed parts)
    P0 = np.zeros((P, P))
    P0[np.arange(T), np.arange(T)] += 1e-4                     # very weak ridge on x
    for s in range(S):
        P0[T + s, T + s] += 1e6 if s == ref else 1 / 100.0     # alpha_ref pinned at 0
        P0[T + S + s, T + S + s] += 1 / dsd[s] ** 2
    sig2 = np.full(S, 0.2 ** 2)
    tau2 = 0.01
    keep = n_iter - n_burn
    X = np.empty((keep, T)); AL = np.empty((keep, S)); DL = np.empty((keep, S))
    SG = np.empty((keep, S)); TAU = np.empty(keep)
    for it in range(n_iter):
        w = 1 / sig2[sidx]
        Q = P0.copy()
        Q[:T, :T] += DtD / tau2
        Q += (A * w[:, None]).T @ A
        b = (A * w[:, None]).T @ yv
        L = np.linalg.cholesky(Q)
        mu = np.linalg.solve(Q, b)
        th = mu + np.linalg.solve(L.T, rng.standard_normal(P))
        x, alpha, delta = th[:T], th[T:T + S], th[T + S:]
        r = yv - A @ th
        for s in range(S):
            rs = r[sidx == s]
            a0, b0 = sigma_prior[s]
            sig2[s] = 1 / rng.gamma(a0 + len(rs) / 2, 1 / (b0 + 0.5 * np.sum(rs ** 2)))
        d2 = D @ x
        a0, b0 = tau_prior
        tau2 = 1 / rng.gamma(a0 + len(d2) / 2, 1 / (b0 + 0.5 * np.sum(d2 ** 2)))
        if it >= n_burn:
            k = it - n_burn
            X[k] = x; AL[k] = alpha; DL[k] = delta; SG[k] = np.sqrt(sig2); TAU[k] = np.sqrt(tau2)
    return {"x": X, "alpha": AL, "delta": DL, "sigma": SG, "tau": TAU}
