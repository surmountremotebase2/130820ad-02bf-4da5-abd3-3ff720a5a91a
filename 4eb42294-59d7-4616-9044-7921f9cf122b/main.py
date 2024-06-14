from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset to watch
        self.ticker = "SPCE"
        
        # Entry/exit thresholds
        self.short_sma_period = 10  # Short-term SMA period
        self.long_sma_period = 50  # Long-term SMA period
        self.profit_target = 1.10  # 10% profit target

        # Keeping track of buy price
        self.buy_price = None  # To keep track of the buy-in price
        
        self.asset_in_portfolio = False  # To check if the asset is currently held

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"  # Use daily intervals for the indicators

    def run(self, data):
        # Get historical closing prices
        closing_prices = [d[self.ticker]["close"] for d in data["ohlcv"]]
        
        # Calculate short-term and long-term SMAs
        short_sma = SMA(self.ticker, data["ohlcv"], self.short_sma_period)
        long_sma = SMA(self.ticker, data["ohlcv"], self.long_sma_period)
        
        # Initializing target allocation
        allocation = {self.ticker: 0}

        if len(closing_prices) > self.long_sma_period:
            # Check for SMA crossover (buy signal)
            if short_sma[-1] > long_sma[-1] and short_sma[-2] < long_sma[-2] and not self.asset_in_portfolio:
                allocation[self.ticker] = 1.0  # Full allocation to SPCE
                self.buy_price = closing_prices[-1]
                self.asset_in_portfolio = True
                log("Buying SPCE at {}".format(self.buy_price))
            
            # Check for a sell condition (take profit)
            if self.asset_in_portfolio:
                current_price = closing_numbers[-1]
                if self.buy_price is not None and current_price >= self.buy_price * self.profit_target:
                    allocation[self.ticker] = 0  # Sell all SPCE holdings
                    log("Taking profit on SPCE at {}".format(current_price))
                    self.asset_in_portfolio = False  # Reset the flag
                    self.buy_price = None  # Reset buy price after selling

        return TargetAllocation(allocation)