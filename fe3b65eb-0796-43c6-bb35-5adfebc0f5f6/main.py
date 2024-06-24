from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    A trading strategy focused on executing take-profit and stop-loss orders for GME and AMC.
    
    The strategy aims to:
    1. Implement a take-profit threshold to lock in profits.
    2. Implement a stop-loss threshold to minimize potential losses.
    3. Recalculate positions daily to adjust to new price movements.
    """

    def __init__(self):
        # Define symbols for GameStop and AMC Entertainment
        self.symbols = ["GME", "AMC"]
        # Define the specific OHLCV data requirements for these stocks
        self.data_requirements = [OHLCV(symbol) for symbol in self.symbols]
        
        # Define take-profit and stop-loss thresholds in percentages (e.g., 10% for take-profit and -5% for stop-loss)
        self.take_profit_threshold = 0.10  # 10% take profit
        self.stop_loss_threshold = -0.05   # 5% stop loss

        # Initial allocations
        self.allocations = {symbol: 0.5 for symbol in self.symbols}  # Starting with an equal distribution

    @property
    def assets(self):
        """
        Specifies the assets required for this strategy.
        """
        return self.symbols

    @property
    def interval(self):
        """
        Specifies the data frequency required by the strategy, set to daily.
        """
        return "1day"

    @property
    def data(self):
        """
        Returns the data requirements for the strategy.
        """
        return self.data_requirements

    def run(self, data):
        """
        Executes the strategy logic including take-profit and stop-loss checks.
        """
        # Looping through each symbol to determine target allocations
        for symbol in self.symbols:
            # Retrieve the latest close price
            latest_close_price = data["ohlcv"][-1][symbol]["close"]
            # Retrieve the previous close price for comparison
            previous_close_price = data["ohlcv"][-2][symbol]["close"]

            # Calculate the price change percentage
            price_change_percentage = (latest_close_price - previous_close_price) / previous_close_price

            log(f"{symbol} price change percentage: {price_change_percentage*100}%")

            # Determine if take-profit or stop-loss should be triggered
            if price_change_percentage >= self.take_profit_threshold:
                # Take profit: Sell the stock
                self.allocations[symbol] = 0
                log(f"Taking profit on {symbol}")
            elif price_change_percentage <= self.stop_loss_threshold:
                # Stop loss: Sell the stock
                self.allocations[symbol] = 0
                log(f"Executing stop loss on {theon}")

        return TargetAllocation(self.allocations)