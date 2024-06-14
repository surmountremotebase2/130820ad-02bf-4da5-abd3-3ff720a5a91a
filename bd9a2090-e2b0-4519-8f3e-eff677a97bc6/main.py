from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.initial_price = 5.0  # Initial price of AMC set at $5
        self.tickers = ["AMC"]  # Define the target asset

    @property
    def assets(self):
        # Return the assets that this strategy acts upon
        return self.tickers

    @property
    def interval(self):
        # Define the interval at which this strategy should be evaluated
        return "1day"

    def run(self, data):
        # Initialize AMC stake to 0 to maintain no position by default
        allocation = {"AMC": 0}

        if "AMC" in data["ohlcv"]:
            # Extract the latest close price of AMC from the data
            latest_close_price = data["ohlcv"][-1]["AMC"]["close"]

            # Calculate the percentage change from the initial price
            percent_change = ((latest, latest_close_price - self.initial_price) / self.initial_price) * 100

            # Determine action based on 5% price movement criteria
            if percent_change > 5:
                # If AMC has moved more than 5% up, sell or reduce position to 0
                allocation["AMC"] = 0  # Indicates selling or not holding the position
                log("AMC has risen more than 5% from initial price, selling/reducing position.")
            elif percent_change < -5:
                # If AMC has moved more than 5% down, initiate or increase buy position
                allocation["AMC"] = 1  # Indicates buying or holding a position
                log("AMC has dropped more than 5% from initial price, buying/increasing position.")

        return TargetAllocation(allocation)