from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, OptionsContract

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["NVDA", "SPCE", "NRDY"]
        self.options_list = []
        # Assuming there is a way to access options contracts in Surmount, pseudo-code below
        for ticker in self.tickers:
            # Find call options for the given tickers, specific to your strategy requirements (e.g., specific strike price, expiration)
            # This is a placeholder for the actual method to fetch options
            self.options_list.extend(self.find_options(ticker, option_type="call"))

    @property
    def interval(self):
        # Checking once a day to avoid pattern day trading
        return "1day"

    @property
    def assets(self):
        # Assets targeted by the strategy
        return self.tickers

    @property
    def data(self):
        # Your data sources; options contracts for the relevant tickers
        return self.options_list

    def find_options(self, ticker, option_type="call"):
        # Placeholder: Implement actual logic to find and filter options based on criteria (strike, expiration, etc.)
        # Returning mock options for the purpose of this example
        return [OptionsContract(ticker, option_type)]

    def run(self, data):
        allocation_dict = {}

        # Loop through each options contract in your strategy
        for option in self.options_list:
            option_data = data[tuple(option)]
            # Check if option exists and has the necessary price information
            if option_data and "current_price" in option_data and "purchase_price" in option_data:
                profit = (option_data["current_price"] - option_data["purchase_price"]) / option_data["purchase_price"]

                # If profit is equal or greater than 20%, prepare to sell
                if profit >= 0.20:
                    log(f"Selling {option} at 20%+ profit")
                    # Assuming selling at 100% of the position
                    allocation_dict[option] = 0
                else:
                    # Hold if below 20% profit
                    log(f"Holding {option}, below 20% profit threshold")
                    # Assuming holding at 100% of the position (no change)
                    allocation_dict[option] = 1
            else:
                # Default to hold if data is missing
                allocation_dict[option] = 1

        return TargetAllocation(allocation_dict)

# Note: This script is a conceptual template and may require adjustments based on the Surmount trading package's specific options trading functionalities, which are not detailed in the examples above.