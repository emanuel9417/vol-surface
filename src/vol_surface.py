#class for volsurface

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from src.option_chain import OptionChain
from src.implied_vol import ImpliedVol

class VolSurface:
    def __init__(self, ticker, r, max_iv = 0.5):
        self.ticker=yf.Ticker(ticker)
        self.ticker_name = ticker
        self.spot = self.ticker.history(period = "1d")["Close"].iloc[-1]
        self.r = r
        self.max_iv = max_iv
        self.df_concat = None
        self.df_surface = None

    def collect_data(self):
        m = self.ticker.options
        df_strike_iv = []
        for i in range(len(m)):
            chain = OptionChain(self.ticker_name, expiry_index = i)
            chain.fetch()
            ivd = ImpliedVol(chain, self.r)
            ivd.compute_iv()
            ivd.build_dataframe()
            ivd.df_strike_iv['Maturity'] = chain.expiry
            df_strike_iv.append(ivd.df_strike_iv)
        self.df_concat = pd.concat((df_strike_iv), ignore_index = True)
        self.df_concat = self.df_concat[self.df_concat['Strike'].between(self.spot * 0.25, self.spot * 1.75)]
        return self

    def pivot(self):
        self.df_surface = self.df_concat.pivot_table(values = 'IV', index = 'Strike', columns = 'Maturity')
        self.df_surface = self.df_surface.interpolate(axis = 1)
        return self

    def surface_plot(self):
        figsurf = go.Figure(data = [go.Surface(x = self.df_surface.columns, y = self.df_surface.index, z = self.df_surface.values)])
        figsurf.update_layout(title = f"Volatility Surface - {self.ticker_name} ", autosize = False, width = 900, height = 700)
        return figsurf