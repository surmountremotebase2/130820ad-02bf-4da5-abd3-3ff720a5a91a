from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers we are interested in
        self.tickers = ["AMC", "GME"]
        # Short-term and long-term window sizes for SMA calculation
        self.short_window = 10
        self.long_window = 30
        
    @property
    def interval(self):
        # Using daily prices for analysis
        return "1day"
    
    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        # No additional data fetching specified beyond default OHLCV
        return []

    def run(self, data):
        # Initialize the target allocation dictionary
        allocation_dict = {}
        
        for ticker in self.tickers:
            # Calculate short-term and long-term SMA
            short_sma = SMA(ticker, data["ohlcv"], self.short_window)
            long_sma = SMA(ticker, data["ohlcv"], self.long_window)

            if len(short_sma) == 0 or len(long_sma) == 0:
                # Information might be insufficient; no action is taken
                allocation_dict[ticker] = 0
                continue

            # Check the SMA crossover; last -1 is the most recent data point
            if short_sma[-1] > long_sma[-1]:
                # Bullish signal
                log(f"Bullish signal for {ticker}")
                allocation_dict[ticker] = 0.5  # Example allocation, adjust based on strategy risk management
            elif short_sma[-1] < long_sma[-1]:
                # Bearish signal
                log(f"Bearish signal for {ticker}")
                allocation_dict[ticker] = 0  # Sell or avoid position
            else:
                # No clear signal; might maintain previous holdings or take no action
                allocation_dict[ticker] = 0  # Example default action

        # Return the target allocation
        return TargetAllocation(allocation_dict)