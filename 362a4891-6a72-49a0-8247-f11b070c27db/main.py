from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Focusing on stable, large-cap stocks
        self.tickers = ["AAPL", "MSFT", "JNJ", "XOM"]
        self.short_window = 40
        self.long_window = 100
    
    @property
    def interval(self):
        # Using daily data for the strategy
        return "1day"
    
    @field
    def assets(self):
        return self.tickers
    
    @property
    def data(self):
        # No additional data required beyond default OHLCV
        return []
    
    def run(self, data):
        allocation_dict = {}
        
        for ticker in self.tickers:
            # Calculate short and long Simple Moving Averages (SMA)
            short_sma = SMA(ticker, data["ohlcv"], self.short_window)
            long_sma = SMA(ticker, data["ohlcv"], self.long_window)
            
            if not short_sma or not long_sma:
                log(f"Insufficient data for {ticker}")
                continue
            
            # Strategy logic: Go long if short SMA is above long SMA, indicating an uptrend
            if short_sma[-1] > long_sma[-1]:
                allocation_dict[ticker] = 1 / len(self.tickers)
            else:
                allocation_dict[ticker] = 0
                
        return TargetAllocation(allocation_dict)