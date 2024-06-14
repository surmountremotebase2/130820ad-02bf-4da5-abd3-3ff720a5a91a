from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "GME"

    @property
    def interval(self):
        # Using daily data to check for significant daily moves
        return "1day"

    @property
    def assets(self):
        # Trading strategy is focused on GME only
        return [self.ticker]

    @property
    def data(self):
        # No additional data needed beyond the default which includes OHLCV
        return []

    def run(self, data):
        """
        Execute the trading strategy for GME based on RSI indicators.
        
        Sells GME when RSI indicates overbought conditions (>70),
        and buys GME when RSI signals oversold conditions (<30).
        """
        # Initialize allocation to hold; consider changing 
        # allocations dynamically based on account value and risk management parameters.
        allocation_dict = {self.ticker: 0}  

        # Calculate the RSI for GME
        rsi_values = RSI(self.ticker, data["ohlcv"], 14)  # Using a 14-day period for RSI calculation

        # Make decisions based on the latest RSI value
        if len(rsi_values) > 0:
            latest_rsi = rsi_values[-1]
            log(f"Latest RSI for {self.ticker}: {latest_rsi}")

            # Conditions to Sell or Buy based on RSI
            if latest_rsi > 70:
                # RSI indicates overbought condition; consider selling
                allocation_dict[self.ticker] = -1  # Assuming possibility to short. Use 0 instead to just sell off holdings
            elif latest_rsi < 30:
                # RSI indicates oversold condition; consider buying
                allocation_dict[self.ticker] = 1  # Allocate 100% of the portfolio to buying GME
                
        return TargetAllocation(allocation_dict)