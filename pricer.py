import numpy as np
from math import log, sqrt, exp
from scipy.stats import norm

class MultiAssetPricer:

    def price(self, product_type, **kwargs):

        if product_type == "bond":
            return self.price_bond(**kwargs)

        elif product_type == "option":
            return self.price_option(**kwargs)

        elif product_type == "eln":
            return self.price_eln(**kwargs)

        else:
            raise ValueError("Unsupported product type")

    # -------------------------
    # Bond Pricing
    # -------------------------
    def price_bond(self, face_value, r, T):
        return face_value / (1 + r) ** T

    # -------------------------
    # Black-Scholes Option
    # -------------------------
    def price_option(self, S, K, T, r, sigma, option_type="call", dividend_yield=0):

        d1 = (log(S / K) + (r - dividend_yield + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)

        if option_type == "call":
            price = S * exp(-dividend_yield * T) * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        else:
            price = K * exp(-r * T) * norm.cdf(-d2) - S * exp(-dividend_yield * T) * norm.cdf(-d1)

        return price

    # -------------------------
    # Monte Carlo ELN Pricing
    # -------------------------
    def price_eln(self, S, r, sigma, T=1, n_sim=10000, coupon=0.1, strike_ratio=0.9):

        np.random.seed(42)
        Z = np.random.standard_normal(n_sim)

        ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

        payoff = np.where(ST >= strike_ratio * S, S * (1 + coupon), ST)

        price = np.exp(-r * T) * np.mean(payoff)

        return price