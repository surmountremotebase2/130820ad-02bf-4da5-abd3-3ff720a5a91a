from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers (assets) to monitor
        self.tickers = ["AAPL", "AMZN", "MSFT", "GOOGL"]
        # Threshold for taking profit (10% gain)
        self.profit_threshold = 0.10
        # Placeholder for initial buying prices (Assuming it's tracked elsewhere)
        # This needs to be updated according to actual purchase price for a real strategy to work
        self.buying_prices = {
            "AAPL": 100,  # Example purchase price
            "AMZN": 200,
            "MSFT": 300,
            "GOOGL": 400
        }

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Set the interval to daily for this strategy
        return "1day"

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            current_price = data["ohlcv"][-1][ticker]["close"]  # Latest closing price
            # Calculate the percentage gain
            gain = (current_price - self.buying_prices[ticker]) / self.buying_prices[ticker]
            if gain >= self.profit_threshold:
                # If gain is 10% or more, set allocation to 0 indicating a sell signal
                allocation_dict[ticker] = 0
                log(f"Taking profit on {ticker}: Current gain {gain:.2%}")
            else:
                # Keep the current allocation if the gain is less than 10%
                # Assuming we have a mechanism outside this strategy that initiates buy orders,
                # here we simply do not change the position.
                # In a complete strategy, consider management of the buy allocations as well.
                allocation_dict[ticker] = 1  # This is a simplified representation

        return TargetAllocation(allocation_dict)