from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    """
    An example trading strategy that buys a stock when RSI is below 30
    indicating it might be oversold and sells when RSI is above 70, indicating
    it might be overbought.
    """
    def __init__(self):
        self.tickers = ["AAPL"]  # Target tickers can be adjusted
        self.rsi_period = 14  # Customizable RSI period

    @property
    def interval(self):
        return "1day"  # Defines the interval for data fetching

    @property
    def assets(self):
        return self.tickers  # Specifies the assets this strategy targets

    def run(self, data):
        """
        The core logic of the strategy that determines target allocations based
        on RSI indicator's signal.

        :param data: The latest market data and indicators
        :return: TargetAllocation object with desired asset allocation
        """
        allocation_dict = {}
        for ticker in self.assets:
            rsi_data = Rsi(ticker, data["ohlcv"], self.rsi_period)  # Calculate RSI
            if rsi_data is None or len(rsi_data) == 0:
                log(f"RSI data is not available for {ticker}. Skipping")
                continue

            current_rsi = rsi_data[-1]  # Latest RSI value
            if current_rsi < 30:
                # Considered oversold; buying opportunity
                allocation_dict[ticker] = 1 / len(self.tickers)  # Equal allocation among tickers
            elif current_rsi > 70:
                # Considered overbought; might be a selling signal
                allocation_dict[ticker] = 0  # No allocation, equivalent to selling
            else:
                # Neutral, no action
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)

if __name__ == "__main__":
    # The strategy can be instantiated and run by the Surmount platform
    strategy = TradingStrategy()