import numpy as np
from dataclasses import dataclass
from typing import Literal

Kind = Literal["call", "put"]

@dataclass
class MCParams:
    S: float; K: float; r: float; sigma: float; T: float
    barrier: float; steps: int; paths: int; seed: int = 42

def mc_down_and_out(kind: Kind, p: MCParams) -> float:
    np.random.seed(p.seed)
    dt = p.T / p.steps
    mu = (p.r - 0.5*p.sigma**2)*dt
    vol = p.sigma*np.sqrt(dt)

    # Antithetic variates
    z = np.random.randn(p.paths//2, p.steps)
    z = np.vstack([z, -z])

    S = np.full((p.paths,), p.S, dtype=float)
    alive = np.ones(p.paths, dtype=bool)

    for t in range(p.steps):
        S[alive] = S[alive]*np.exp(mu + vol*z[alive, t])
        alive &= (S > p.barrier)

    if kind=="call":
        payoff = np.maximum(S - p.K, 0.0)
    else:
        payoff = np.maximum(p.K - S, 0.0)
    payoff[~alive] = 0.0  # knocked out
    disc = np.exp(-p.r*p.T)
    return disc*payoff.mean()

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["call","put"], required=True)
    ap.add_argument("--S", type=float, required=True)
    ap.add_argument("--K", type=float, required=True)
    ap.add_argument("--r", type=float, required=True)
    ap.add_argument("--sigma", type=float, required=True)
    ap.add_argument("--T", type=float, required=True)
    ap.add_argument("--barrier", type=float, required=True)
    ap.add_argument("--steps", type=int, default=252)
    ap.add_argument("--paths", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    p = MCParams(args.S,args.K,args.r,args.sigma,args.T,args.barrier,args.steps,args.paths,args.seed)
    print(f"down-and-out {args.kind} ≈ {mc_down_and_out(args.kind, p):.6f}")