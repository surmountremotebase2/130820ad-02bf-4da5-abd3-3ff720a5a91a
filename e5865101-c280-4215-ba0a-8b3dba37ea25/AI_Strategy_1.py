from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log


class TradingStrategy(Strategy):

    def __init__(self):
        # Define the ticker for Bitcoin; the actual ticker symbol might
        # vary depending on the data provider you're using (e.g., "BTC-USD" for Yahoo Finance)
        self.ticker = "BTC"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Extracts the closing prices for the BTC asset
        close_prices = [i[self.ticker]["close"] for i in data["ohlcv"]]

        # Calculates the short and long moving averages
        short_ma = SMA(self.ticker, data["ohlcv"], length=10)
        long_ma = SMA(self.ticker, data["ohlcv"], length=50)

        # Initializes the allocation with no position
        allocation = {self.ticker: 0}

        if len(short_ma) > 0 and len(long_ma) > 0:
            latest_short_ma = short_ma[-1]
            latest_long_ma = long_ma[-1]

            # If the short MA crosses above the long MA, buy (allocate 100% to BTC)
            if latest_short_ma > latest_long_ma:
                allocation[self.ticker] = 1.0
                log("Going long")

            # If the short MA crosses below the long MA, sell (allocate 0% to BTC)
            elif latest_short_ma < latest_long_ma:
                allocation[self.ticker] = 0
                log("Going short")

        return TargetAllocation(allocation)