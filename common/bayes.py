"""A small, transparent Bayesian toolkit (numpy and scipy only) shared by the chart models.

Everything here is deliberately simple so a reader can audit it:
  * metropolis(): an adaptive random-walk Metropolis sampler for low-dimensional posteriors, run as four chains so
    convergence can be checked with the Gelman-Rubin R-hat statistic (rhat()). Used by Charts 6, 8 and 10.
  * lognormal_interval_loglik() and lognormal_interval_fit(): a log-normal population fitted to durations that are
    known only as intervals, or as 'has not happened yet' (right-censored). Used by Chart 6, and through it Chart 10.
  * beta_from_q(), beta_from_q3(), lognormal_from_q(): turn a stated low / central / high judgement into a Beta or a
    log-normal distribution. Used by Chart 4.
"""
from __future__ import annotations

import numpy as np
from scipy import stats


# --------------------------------------------------------------------------------------- MCMC
def metropolis(logp, x0, n_iter=20000, n_burn=5000, n_chains=4, init_scale=0.1, seed=0, thin=5):
    """Adaptive random-walk Metropolis. logp(theta)->float. Returns (samples[chains*kept, d], rhat[d], acc)."""
    x0 = np.atleast_1d(np.asarray(x0, float))
    d = x0.size
    rng = np.random.default_rng(seed)
    out, accs = [], []
    for c in range(n_chains):
        x = x0 + rng.normal(0, init_scale, d)
        lp = logp(x)
        tries = 0
        while not np.isfinite(lp) and tries < 200:
            x = x0 + rng.normal(0, init_scale, d)
            lp = logp(x)
            tries += 1
        cov = np.eye(d) * init_scale ** 2
        chain = np.empty((n_iter, d))
        acc = 0
        hist = []
        for i in range(n_iter):
            if i < n_burn and i > 500 and i % 250 == 0:
                h = np.array(hist[-2000:])
                cov = np.cov(h.T).reshape(d, d) * (2.38 ** 2 / d) + np.eye(d) * 1e-8
            prop = rng.multivariate_normal(x, cov)
            lpp = logp(prop)
            if np.log(rng.random()) < lpp - lp:
                x, lp = prop, lpp
                if i >= n_burn:
                    acc += 1
            chain[i] = x
            hist.append(x.copy())
        kept = chain[n_burn::thin]
        out.append(kept)
        accs.append(acc / max(1, n_iter - n_burn))
    arr = np.stack(out)                       # chains x draws x d
    return arr.reshape(-1, d), rhat(arr), float(np.mean(accs))


def rhat(arr):
    """Gelman-Rubin potential scale reduction factor for chains x draws x d."""
    m, n, d = arr.shape
    means = arr.mean(axis=1)
    W = arr.var(axis=1, ddof=1).mean(axis=0)
    B = n * means.var(axis=0, ddof=1)
    var_hat = (n - 1) / n * W + B / n
    return np.sqrt(var_hat / W)


# --------------------------------------------------------------------------------------- judgement -> distribution
def lognormal_from_q(lo, hi, p=0.8):
    """(mu, sigma) of a lognormal whose central p-interval is [lo, hi]."""
    z = stats.norm.ppf(0.5 + p / 2)
    mu = (np.log(lo) + np.log(hi)) / 2
    sigma = (np.log(hi) - np.log(lo)) / (2 * z)
    return mu, sigma


def beta_from_q(lo, hi, p=0.8):
    """Beta(a,b) whose central p-interval approximately matches [lo, hi] (moment matching on logit scale)."""
    from scipy.optimize import minimize
    target = np.array([lo, hi])
    qs = np.array([0.5 - p / 2, 0.5 + p / 2])

    def loss(v):
        a, b = np.exp(v)
        return np.sum((stats.beta.ppf(qs, a, b) - target) ** 2)

    m = (lo + hi) / 2
    res = minimize(loss, np.log([m * 10, (1 - m) * 10]), method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-10})
    return tuple(np.exp(res.x))


def beta_from_q3(lo, mid, hi, p=0.8):
    """Beta(a,b) whose 10th, 50th and 90th percentiles best match (lo, mid, hi) in least squares."""
    from scipy.optimize import minimize
    qs = np.array([0.5 - p / 2, 0.5, 0.5 + p / 2])
    target = np.array([lo, mid, hi])

    def loss(v):
        a, b = np.exp(v)
        return np.sum((stats.beta.ppf(qs, a, b) - target) ** 2)

    best = None
    for s in (4, 10, 30):
        res = minimize(loss, np.log([mid * s, (1 - mid) * s]), method="Nelder-Mead",
                       options={"xatol": 1e-7, "fatol": 1e-12, "maxiter": 4000})
        if best is None or res.fun < best.fun:
            best = res
    return tuple(np.exp(best.x))


# --------------------------------------------------------------------------------------- censored durations
def lognormal_interval_loglik(lo, hi, mu, sigma):
    """Interval-censored lognormal: each observation known to lie in [lo, hi] (hi may be inf; lo==hi exact)."""
    lo = np.asarray(lo, float)
    hi = np.asarray(hi, float)
    exact = np.isclose(lo, hi)
    ll = np.zeros_like(lo)
    if exact.any():
        ll[exact] = stats.lognorm.logpdf(lo[exact], s=sigma, scale=np.exp(mu))
    ie = ~exact
    if ie.any():
        cdf_hi = np.where(np.isinf(hi[ie]), 1.0, stats.lognorm.cdf(np.where(np.isinf(hi[ie]), 1.0, hi[ie]), s=sigma,
                                                                    scale=np.exp(mu)))
        cdf_lo = stats.lognorm.cdf(lo[ie], s=sigma, scale=np.exp(mu))
        ll[ie] = np.log(np.clip(cdf_hi - cdf_lo, 1e-300, None))
    return float(np.sum(ll))


def lognormal_interval_fit(lo, hi, prior_mu=0.0, prior_mu_sd=2.0, prior_sigma_scale=1.5, n_iter=20000,
                           n_burn=5000, seed=5):
    """Posterior for (mu, sigma) of a lognormal population given interval-censored observations [lo, hi].

    Used for the adoption lags of Chart 6 (and, through its draws, Chart 10): observed lags enter as intervals, techniques
    that have not yet scaled enter as 'at least this long' (hi = inf).
    """
    lo = np.asarray(lo, float)
    hi = np.asarray(hi, float)

    def logp(th):
        mu, logs = th
        s = np.exp(logs)
        if not (0.05 < s < 6):
            return -np.inf
        ll = lognormal_interval_loglik(lo, hi, mu, s)
        lp = stats.norm.logpdf(mu, prior_mu, prior_mu_sd) + stats.halfnorm.logpdf(s, scale=prior_sigma_scale) + logs
        return ll + lp

    draws, rh, acc = metropolis(logp, np.array([prior_mu, np.log(0.8)]), n_iter=n_iter, n_burn=n_burn, n_chains=4,
                                init_scale=0.2, seed=seed)
    return {"mu": draws[:, 0], "sigma": np.exp(draws[:, 1]), "rhat": rh, "acc": acc}
