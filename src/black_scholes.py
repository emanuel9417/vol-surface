import numpy as np
from scipy.stats import norm

def calculate_d1_d2(S, K, r, T, sigma):

    d1 = (np.log(S/K) + (r + sigma**2/2) * T)/(sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    return(d1,d2)

def bs_pricer(S, K, r, T, sigma, option_type):
    
    d1, d2 = calculate_d1_d2(S, K, r, T, sigma)
    
    option_type = option_type.lower().strip()
    
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return(round(price, 5))