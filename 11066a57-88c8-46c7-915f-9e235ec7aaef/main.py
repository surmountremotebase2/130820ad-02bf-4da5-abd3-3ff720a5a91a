from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker of the asset you're trading
        # This example uses "AAPL" as an example; replace it with any stock you're interested in.
        self.ticker = "AAPL"
        
        # Define the initial purchase price for the asset.
        # In a live strategy, this might be dynamically set based on actual purchase price.
        # For demonstration purposes, it's hardcoded.
        self.purchase_price = 100  # assuming the purchase price was $100
        
        # Define the target profit percentage (e.g., 10%)
        self.profit_target = 0.10

    @property
    def interval(self):
        # Define the interval at which the strategy checks the price.
        # This can be adjusted based on your trading frequency preference.
        return "1day"

    @property
    def assets(self):
        # List the assets involved in this strategy. 
        # This example strategy works with a single asset.
        return [self.ticker]

    def run(self, data):
        # Initialize an empty allocation dictionary
        allocation_dict = {self.ticker: 0}
        
        # Check if there is enough data for the asset
        if self.ticker in data["ohlcv"]:
            # Get the current close price of the ticker
            current_price = data["ohlcv"][-1][self.ticker]["close"]
            
            # Calculate the current profit based on the purchase price and the current price
            profit = (current_price - self.purchase_price) / self.purchase_price
            
            # Check if the profit has reached the target profit
            if profit >= self.profit_target:
                log(f"Target profit reached for {self.ticker}. Current profit: {profit*100}%. Selling.")
                allocation_dict[self.ticker] = 0  # Signal to sell
            else:
                log(f"Target profit not reached for {self.ticker}. Holding.")
                allocation_dict[self.ticker] = 1  # Signal to hold
        else:
            log("No data available for the specified ticker.")
        
        return TargetAllocation(allocation_dict)