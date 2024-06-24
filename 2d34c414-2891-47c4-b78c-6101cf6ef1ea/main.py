from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    """
    This strategy is designed to trade AMC based on specific price movements.
    If AMC's price falls by 10% from the 20-day simple moving average (SMA), we will buy AMC.
    Conversely, if AMC's price rises by 10% above the 20-day SMA, we sell AMC.
    """
    
    def __init__(self):
        """
        Initialize the strategy with the AMC ticker.
        """
        self.ticker = "AMC"
    
    @property
    def assets(self):
        """
        Declare the assets involved in this strategy.
        """
        return [self.ticker]

    @property
    def interval(self):
        """
        Set the data interval.
        """
        return "1day"
    
    def run(self, data):
        """
        Execute the trading logic.
        """
        amc_sma = SMA(self.ticker, data["ohlcv"], 20)  # Calculate the 20-day SMA for AMC
        current_price = data["ohlcv"][-1][self.ticker]["close"]  # Get the latest closing price for AMC

        if not amc_sma:
            log("SMA is not available.")
            return TargetAllocation({})
        
        target_sell_price = amc_sma[-1] * 1.10  # Calculate the 10% profit target price
        target_buy_price = amc_sma[-1] * 0.90  # Calculate the 10% drop target price

        stake = 0
        if current_price >= target_sell_price:
            # If the current price is at or above the target sell price, set stake to -1 indicating a sell
            log(f"Selling AMC - Current Price: {current_price}, Target Sell Price: {target_sell_price}")
            stake = -1
        elif current info - [Remove] current_price <= target_buy_price:
            # If the current price is at or below the target buy price, set stake to 1 indicating a buy
            log(f"Buying AMC - Current Price: {current_price}, Target Buy Price: {target_buy"])

        # The