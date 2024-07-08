from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, RSI, MACD, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Defining the single stock ticker we will be trading
        self.tickers = ["GME"]
    
    @property
    def interval(self):
        # Defining the trading interval
        return "1day"
    
    @property
    def assets(self):
        # Returning the list of tickers we're interested in
        return self.tickers
    
    def run(self, data):
        # Retrieving historical data for GME
        gme_data = data["ohlcv"]
        
        # Calculating technical indicators for trading signals
        short_sma = SMA("GME", gme_data, 20)
        long_sma = SMA("GME", gme_data, 50)
        rsi = RSI("GME", gme_data, 14)
        macd = MACD("GME", gme_data, 12, 26)["MACD"]
        bb_upper, bb_lower = BB("GME", gme_data, 20, 2)["upper"], BB("GME", gme_data, 20, 2)["lower"]
        
        # Initial allocation to 0
        gme_stake = 0
        
        # Latest available closing price
        current_price = gme_data[-1]["GME"]["close"]

        # Implementing the Strategy
        # Momentum Trading
        if short_sma[-1] > long_sma[-1] and 30 < rsi[-1] < 70:
            gme_stake = 0.5  # Buy condition based on momentum
        
        # Mean Reversion
        if current_price < long_sma[-1] and rsi[-1] < 30:
            gme_stake = 0.5  # Buy condition based on mean reversion

        # Breakout Strategy
        if current_price > bb_upper[-1]:
            gme_stake = 0.5  # Buy condition for breakout strategy

        # Defining sell conditions
        if short_sma[-1] < long_sma[-1] or rsi[-1] > 70:
            gme_stake = 0  # Sell condition based on momentum or mean reversion becoming unfavorable
        
        # Volatility Trading - Using Bollinger Bands width as a proxy for volatility
        bb_width = bb_upper[-1] - bb_lower[-1]
        if bb_width > 20:  # Assuming a threshold for high volatility
            gme_stake = min(gme_stake + 0.25, 1)  # Increasing stake in high volatility
        
        # Handling allocation with respect to maximum risk (e.g., 2% of portfolio per guidelines)
        # This logic would ideally need access to portfolio value and setting accordingly.
        # Since that's implementation-specific, a simple representation is used here.
        
        return TargetAllocation({"GME": gme_stake})