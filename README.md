# Option Pricer (Black–Scholes + Monte Carlo)

Tiny, interview-ready repo showing **clean implementation, tests, and docs**.

## Features
- Black–Scholes closed-form for European calls/puts
- Greeks: Delta, Gamma, Vega, Theta, Rho
- Monte Carlo pricing for **barrier options** (down-and-out) with antithetic variates
- Unit tests with `pytest`
- Simple CLI usage

## Quickstart
```bash
pip install -r requirements.txt
pytest -q
python bs_pricer.py --kind call --S 100 --K 100 --r 0.02 --sigma 0.20 --T 1.0
python mc_barrier.py --S 100 --K 100 --r 0.02 --sigma 0.20 --T 1.0 --barrier 90 --steps 252 --paths 20000
```

## Why this repo (for recruiters)
- Shows **numerical stability**, vectorization, and tests.
- Clean API & docstrings; reproducible results with seeds.
- Easy to skim in 2 minutes; clear README and examples.
