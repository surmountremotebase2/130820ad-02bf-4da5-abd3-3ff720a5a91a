from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "NVDA"
        # Define a short and long moving averages period
        self.short_window = 20
        self.long_window = 50 
        # Placeholder for data requirements
        self.data_list = []

    @property
    def interval(self):
        # Execution interval for the strategy
        return "1day"
    
    @property
    def assets(self):
        # Focus on NVDA stock
        return [self.ticker]

    @property
    def data(self):
        # Data requirements (Technical indicators)
        return self.data_list

    def run(self, data):
        # Assess if sufficient data is available
        if len(data["ohlcv"]) < self.long_window:
            # Not enough data to run strategy
            return TargetAllocation({self.ticker: 0})

        # Calculate moving averages
        short_ma = SMA(self.ticker, data["ohlcv"], self.short_window)
        long_ma = SMA(self.ticker, data["ohlcv"], self.long_window)

        # Determine NVDA stake based on moving average crossover
        nvda_stake = 0
        if short_ma[-1] > long_ma[-1] and short_ma[-2] < long_ma[-2]:
            # Golden cross - signal to go long
            nvda_stake = 1
        elif short_ma[-1] < long_ma[-1] and short_ma[-2] > long_ma[-2]:
            # Death cross - signal to exit or go short
            nvda_stake = 0  # For simplicity, we do not implement short-selling in this example

        return TargetAllocation({self.ticker: nvda_stake})