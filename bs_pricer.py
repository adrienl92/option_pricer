import math
from dataclasses import dataclass
from typing import Literal
from math import log, sqrt, exp
from scipy.stats import norm

Kind = Literal["call", "put"]

@dataclass
class BSParams:
    S: float     # spot
    K: float     # strike
    r: float     # risk-free rate
    sigma: float # volatility
    T: float     # time to maturity (years)

def _d1d2(params: BSParams):
    S,K,r,sigma,T = params.S, params.K, params.r, params.sigma, params.T
    d1 = (log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    return d1,d2

def price(kind: Kind, params: BSParams) -> float:
    d1, d2 = _d1d2(params)
    S,K,r,sigma,T = params.S, params.K, params.r, params.sigma, params.T
    if kind == "call":
        return S*norm.cdf(d1) - K*exp(-r*T)*norm.cdf(d2)
    else:
        return K*exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

def delta(kind: Kind, params: BSParams) -> float:
    d1,_ = _d1d2(params)
    return norm.cdf(d1) if kind=="call" else norm.cdf(d1)-1.0

def gamma(params: BSParams) -> float:
    d1,_ = _d1d2(params)
    return norm.pdf(d1)/(params.S*params.sigma*sqrt(params.T))

def vega(params: BSParams) -> float:
    d1,_ = _d1d2(params)
    return params.S*norm.pdf(d1)*sqrt(params.T)

def theta(kind: Kind, params: BSParams) -> float:
    d1,d2 = _d1d2(params)
    S,K,r,sigma,T = params.S, params.K, params.r, params.sigma, params.T
    term1 = - (S*norm.pdf(d1)*sigma)/(2*sqrt(T))
    if kind=="call":
        return term1 - r*K*math.exp(-r*T)*norm.cdf(d2)
    else:
        return term1 + r*K*math.exp(-r*T)*norm.cdf(-d2)

def rho(kind: Kind, params: BSParams) -> float:
    _,d2 = _d1d2(params)
    K,r,T = params.K, params.r, params.T
    if kind=="call":
        return K*T*math.exp(-r*T)*norm.cdf(d2)
    else:
        return -K*T*math.exp(-r*T)*norm.cdf(-d2)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--kind", choices=["call","put"], required=True)
    p.add_argument("--S", type=float, required=True)
    p.add_argument("--K", type=float, required=True)
    p.add_argument("--r", type=float, required=True)
    p.add_argument("--sigma", type=float, required=True)
    p.add_argument("--T", type=float, required=True)
    args = p.parse_args()
    params = BSParams(args.S,args.K,args.r,args.sigma,args.T)
    val = price(args.kind, params)
    print(f"{args.kind} price = {val:.6f}")