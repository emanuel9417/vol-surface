import yfinance as yf

class OptionChain:
    def __init__(self, ticker, expiry_index = 0):
        self.ticker = yf.Ticker(ticker)
        self.spot = self.ticker.history(period = "1d")["Close"].iloc[-1]
        self.expiry = self.ticker.options[expiry_index]
        self.calls = None
        self.puts = None

    def fetch(self):
        option_chain = self.ticker.option_chain(self.expiry)
        self.calls = option_chain.calls
        self.puts = option_chain.puts
        return self

    def clean(self, min_oi = 0, min_volume = 1):
        self.calls = self._filter(self.calls, min_oi, min_volume)
        self.puts = self._filter(self.puts, min_oi, min_volume)
        return self

    def _filter(self, df, min_oi, min_volume):
        df = df[df['openInterest'] > min_oi]
        df = df[df['volume'] > min_volume]
        return df