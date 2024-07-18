from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker of interest
        self.ticker = "AAPL"

    @property
    def assets(self):
        # Specify the asset(s) that the strategy will trade
        return [self.ticker]

    @property
    def interval(self):
        # Set the time interval for data collection, here we use daily data
        return "1day"

    def run(self, data):
        # Initialize the target allocation with no position
        allocation_dict = {self.ticker: 0}
        
        # Calculate the RSI for the specified ticker
        rsi_values = RSI(self.ticker, data["ohlcv"], 14) # 14 periods
        
        # Check if we have enough data to compute the RSI
        if rsi_values is not None and len(rsi_values) > 0:
            current_rsi = rsi_values[-1]
            
            if current_rsi < 30:
                # If RSI is below 30, indicating the asset might be oversold, allocate 100% to this asset
                log(f"RSI is {current_rsi}, considered oversold. Buying {self.ticker}.")
                allocation_dict[self.ticker] = 1
            elif current_rsi > 70:
                # If RSI is above 70, it suggests the asset is potentially overbought
                log(f"RSI is {current_rsi}, considered overbought. Selling {self.ticker}.")
                # Zero allocation to sell the position
                allocation_dict[self.ticker] = 0
            else:
                # If RSI is between 30 and 70, take no action
                log(f"RSI is {current_rsi}, within neutral range. Holding {self.ticker}.")

        return TargetAllocation(allocation_dict)