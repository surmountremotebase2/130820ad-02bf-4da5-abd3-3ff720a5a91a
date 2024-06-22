from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset we're trading
        self.asset = "AMC"
        # Assuming an attribute to store the original purchase price
        # This should be set to your buy-in price or obtained programmatically
        self.purchase_price = 10  # Placeholder value, replace with actual buy price
        
        # Adjust this factor to change the target profit (e.g., 0.1 for 10%)
        self.profit_target = 0.1

    @property
    def interval(self):
        # Define the data interval
        return "1day"

    @property
    def assets(self):
        # Define which asset(s) this strategy concerns
        return [self.asset]

    @property
    def data(self):
        # Specify the data required by the strategy
        # OHLCV data for the asset for price checks
        return [OHLCV(self.asset)]

    def run(self, data):
        # Initialize allocation with a default 'hold' 
        allocation_dict = {self.asset: 1}

        # Check if we have enough data points (at least 1 day)
        if len(data["ohlcv"]) > 0:
            # Latest price data for AMC
            current_price = data["ohlcv"][-1][self.asset]["close"]
            
            # Calculate profit ratio
            profit_ratio = (current_price - self.purchase_price) / self.purchase - self.purchase_price
            
            # Check if profit target met or exceeded
            if profit_ratio >= self.profit_target:
                # Set allocation to 0 to indicate selling off the position
                allocation_dict[self.asset] = 0
        
        return TargetAllocation(allocation_dict)