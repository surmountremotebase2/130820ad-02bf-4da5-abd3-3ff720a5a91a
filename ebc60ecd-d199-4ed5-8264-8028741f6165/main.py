from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, RSI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AMC"  # Focused on trading AMC stock

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"  # Using daily intervals for swing trading

    def run(self, data):
        allocation = 0  # Default to no position
        d = data["ohlcv"]  # Access historical data

        # Ensure there's enough data to compute indicators
        if len(d) > 50:
            # Technical Indicators
            sma_short = SMA(self.ticker, d, 20)[-1]
            sma_long = SMA(self.ticker, d, 50)[-1]
            rsi = RSI(self.ticker, d, 14)[-1]
            bb = BB(self.ticker, d, 20, 2)  # Using standard deviation of 2 for Bollinger Bands

            current_price = d[-1][self.ticker]["close"]

            # Momentum Trading Signals
            if sma_short > sma_long and 30 < rsi < 70:
                # Buy signal based on moving average crossover and RSI conditions
                allocation = 0.2  # 20% of capital allocated
            elif sma_short < sma_long or rsi > 70:
                # Sell signal based on moving average crossover or RSI conditions
                allocation = 0

            # Mean Reversion and Breakout Strategies
            if current_price < sma_long and rsi < 30:
                # Buy signal for mean reversion
                allocation = 0.2
            elif current_price > bb['upper'][-1]:
                # Buy signal for breakout above upper Bollinger Band
                allocation = 0.2
            elif current_price < bb['lower'][-1] and rsi > 70:
                # Sell signal based on price moving back inside Bollinger Bands or high RSI
                allocation = 0

            # Adjust the allocation based on volatility and other market factors in further development

        return TargetAllocation({self.ticker: allocation})