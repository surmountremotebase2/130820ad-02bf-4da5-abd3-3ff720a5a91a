from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TSLA"]
        self.holding_period = 0  # Tracks holding period to avoid pattern day trading

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        # Note: OHLCV data is automatically included and does not need to be explicitly added to data_list.
        return []

    def run(self, data):
        # Ensure there's enough data for analysis
        if len(data['ohlcv']) < 2:
            return TargetAllocation({})

        # Get the last two days of closing prices
        close_prices = [data['ohlcv'][-2][self.tickers[0]]['close'], data['ohlcv'][-1][self.tickers[0]]['close']]

        # Calculate the percentage change between the last two days
        daily_gain = (close_prices[-1] - close_prices[-2]) / close_prices[-2]

        # Decision to invest based on positive gain and compliance with holding period
        if daily_gain > 0 and self.holding_period > 1:
            allocation = 1.0  # All-in if there was a gain in the previous day
            self.holding_period = 0  # Reset holding period after deciding to trade
        else:
            allocation = 0  # No investment if there was no gain
            self.holding_period += 1  # Increment holding period for compliance

        # Log the strategy decision
        log(f"Daily Gain: {daily_gain*100:.2f}%, Allocation: {allocation*100:.2f}%")

        return TargetAllocation({self.tickers[0]: allocation})