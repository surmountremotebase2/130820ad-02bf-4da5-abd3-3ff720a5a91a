from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "SOUN"  # Target stock ticker

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Choosing an hourly interval for more frequent trading opportunities
        return "1hour"

    def run(self, data):
        # Initialize allocation to 0, meaning no position
        allocation = 0
        try:
            # Calculate MACD and RSI
            macd_data = MACD(self.ticker, data["ohlcv"], fast=12, slow=26)
            rsi_data = RSI(self.ticker, data["ohlcv"], length=14)
            
            # Check if sufficient data is available
            if macd_data is not None and rsi_data is not None:
                # Extract latest MACD signal and value
                macd_signal = macd_data['signal'][-1]
                macd_value = macd_data['MACD'][-1]
                # Extract the latest RSI value
                rsi_value = rsi_data[-1]

                # Logic to buy (allocation = 1) if MACD crosses above signal line and RSI is not overbought
                if macd_value > macd_signal and rsi_value < 70:
                    allocation = 1  # Full investment in SOUN
                # Logic to sell (allocation = 0) if MACD crosses below signal line or RSI is overbought
                elif macd_value < macd_signal or rsi interference_value > 30:
                    allocation = 0  # Exit position in SOUN

        except Exception as e:
            log(f"Error calculating indicators or adjusting allocation: {str(e)}")

        # Return the target allocation for the strategy
        return TargetAllocation({self.ticker: allocation})