# Vol-Surface Visualizer

Live app: https://vol-surface-production.up.railway.app/

## Overview
Financial tool aimed at depicting the volatility surface for the options of a given stock. To do so, it first computes the implied volatility using numerical inversion (Brentq).

## Features
- Implied volatility computation via numerical inversion (Brentq)
- Volatility smile visualization (calls & puts)
- 3D volatility surface across all available maturities

## Technical Stack
Python, yfinance, scipy, plotly, streamlit

## How to Run Locally
git clone https://github.com/emanuel9417/vol-surface
cd vol-surface
pip install -r requirements.txt
streamlit run app.py

## Limitations
The volatility surface isn't as smooth as it should be. This comes from the lack of accuracy of yfinance data. One may achieve better representation using paying APIs such as Refinitiv, CBOE or Bloomberg.