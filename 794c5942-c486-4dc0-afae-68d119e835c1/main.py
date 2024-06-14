from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "BTC"
        
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        """Implements the trading strategy logic"""
        
        # Get the MACD indicator data
        macd_data = MACD(self.ticker, data["ohlcv"], 12, 26)
        
        # Calculate current MACD and Signal values
        macd = macd_data["MACD"][-1]
        signal = macd_data["signal"][-1]
        
        allocation_dict = {}
        
        # Check if MACD crossed above Signal line for a buy signal
        if macd > signal:
            log("MACD crossed above Signal. Buy signal.")
            allocation_dict[self.ticker] = 1.0  # 100% allocation
        # Check if MACD crossed below Signal line for a sell signal
        elif macd < signal:
            log("MACD crossed below Signal. Sell signal.")
            allocation_dict[self.ticker] = 0  # 0% allocation, effectively selling
        else:
            log("No trade signal.")
            allocation_dict[self.ticker] = 0
        
        return TargetAllocation(allocation_dict)