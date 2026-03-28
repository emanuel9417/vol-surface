class ImpliedVol:
    def __init__(self, option_chain, r, max_iv = 0.5):
        self.option_chain = option_chain
        self.spot = self.option_chain.spot
        self.expiry = self.option_chain.expiry
        self.r = r
        self.max_iv = max_iv
        self.df_strike_iv = None
        self.calls_strikes = None
        self.calls_iv = None
        self.puts_strikes = None 
        self.puts_iv = None
    
    def compute_iv(self):
        self.calls_strikes, self.calls_iv = self._compute_iv_for_chain(self.option_chain.calls, "call")
        self.puts_strikes, self.puts_iv = self._compute_iv_for_chain(self.option_chain.puts, "put")
        return self

    def _compute_iv_for_chain(self, df, option_type):
        self.expiry_date = datetime.strptime(self.expiry, "%Y-%m-%d")
        T = (self.expiry_date.date() - datetime.now().date()).days/365
        iv_list = []
        strike_list = []
        for i, row in df.iterrows():
            try:
                K = row['strike']
                market_price = row['lastPrice']
                def objective(sigma):
                    return bs_pricer(self.spot, K, self.r, T, sigma, option_type) - market_price
                iv = brentq(objective, 1e-6, 5.0)
                iv_list.append(iv)
                strike_list.append(K)
            except:
                iv_list.append(None)
                strike_list.append(None)
        return strike_list, iv_list

    def build_dataframe(self):
        self.df_strike_iv = pd.DataFrame({'Strike': self.calls_strikes + self.puts_strikes, 'IV':self.calls_iv + self.puts_iv, 'option_type': ['call'] * len(self.calls_strikes) + ['put'] * len(self.puts_strikes)})
        self.df_strike_iv = self.df_strike_iv[self.df_strike_iv['IV'] < self.max_iv]
        return self

    def plot_smile(self):
        fig = px.line(self.df_strike_iv, x= 'Strike', y = 'IV', title = "Volatility Smile - AAPL", color = 'option_type', markers = True, width = 1000, height = 500)
        fig.update_layout(yaxis_tickformat ='.0%')
        fig.add_vline(x = self.spot, annotation_text = "ATM")
        fig.show()