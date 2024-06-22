from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"
        
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"  # Daily intervals to check the RSI

    def run(self, data):
        # Simplified to checking if data exists for brevity
        if not data or self.ticker not in data["ohlcv"]:
            return TargetAllocation({self.ticker: 0})
        
        current_data = data["ohlcv"]
        
        # Calculate the RSI with a window of 14 days which is traditional
        rsi_values = RSI(self.ticker, current_data, 14)
        
        # Thresholds for RSI to consider asset oversold or overbought
        oversold_threshold = 30
        overbought_threshold = 70
        
        last_rsi = rsi_values[-1] if rsi_values else None
        
        allocation = 0  # Default to not holding the asset
        
        # Decide on the allocation based on RSI value
        if last_rsi:
            if last_rsi < oversold_threshold:
                log(f"RSI is below {oversold_threshold}, indicating {self.ticker} is potentially oversold. Consider buying.")
                allocation = 1  # If oversold, allocate 100% to this asset
            elif last_rsi > overbought_threshold:
                log(f"RSI is above {overbought_threshold}, indicating {self.ticker} is potentially overbought. Consider selling.")
                allocation = 0  # If overbought, sell off this asset

        return TargetAllocation({self.ticker: allocation})