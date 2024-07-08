from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "GME"
    
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"
    
    def run(self, data):
        # Ensure enough data is available for technical analysis
        if len(data["ohlcv"]) < 50:  # Considering 50 days for the long-term SMA
            return TargetAllocation({self.ticker: 0})
        
        # Technical Indicators Calculation
        sma_short = SMA(self.ticker, data["ohlcv"], 20)[-1]
        sma_long = SMA(self.ticker, data["ohlcv"], 50)[-1]
        rsi = RSI(self.ticker, data["ohlcv"], 14)[-1]
        bb = BB(self.ticker, data["ohlcv"], 20, 2)
        
        current_price = data["ohlcv"][-1][self.ticker]["close"]
        upper_band = bb["upper"][-1]
        lower_band = bb["lower"][-1]
        
        # Strategy Logic
        
        # Momentum Trading Signal
        if sma_short > sma_long and 30 < rsi < 70:
            allocation = 1.0  # Full allocation
        # Mean Reversion or Oversold Buy Signal
        elif current_price < lower_band and rsi < 30:
            allocation = 0.5  # Conservative allocation, considering risk management
        # Exit condition or take profit
        elif current_price > upper_band or rsi > 70:
            allocation = 0  # Exit position
        else:
            allocation = 0  # Default action is no allocation

        # This will create a TargetAllocation object with the allocation for GME
        return TargetAllocation({self.ticker: allocation})