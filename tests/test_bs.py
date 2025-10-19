from bs_pricer import BSParams, price, delta, gamma, vega, theta, rho

def test_price_symmetry():
    p = BSParams(100, 100, 0.0, 0.2, 1.0)
    # Put-Call parity at r=0 simplifies to: C - P = S - K
    c = price("call", p)
    pu = price("put", p)
    assert abs((c - pu) - (p.S - p.K)) < 1e-6

def test_greeks_signs():
    p = BSParams(100, 100, 0.01, 0.2, 1.0)
    assert delta("call", p) > 0
    assert delta("put", p) < 0
    assert gamma(p) > 0
    assert vega(p) > 0
