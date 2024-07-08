from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, RSI, MACD, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # AMC stock ticker
        self.tickers = ["AMC"]

    @property
    def assets(self):
        # Assets to trade
        return self.tickers

    @property
    def interval(self):
        # Using daily data for swing trading strategy
        return "1day"

    def run(self, data):
        # Initialize AMC stake to 0
        amc_stake = 0

        # Short-term and long-term Simple Moving Averages
        sma_short = SMA("AMC", data["ohlcv"], 20)
        sma_long = SMA("AMC", data["ohlcv"], 50)

        # Relative Strength Index
        rsi = RSI("AMC", data["ohlcv"], 14)

        # MACD
        macd_data = MACD("AMC", data["ohlcv"], fast=12, slow=26)
        macd_line = macd_data["MACD"] if "MACD" in macd_data else []
        signal_line = macd_data["signal"] if "signal" in macd_data else []

        # Bollinger Bands
        bollinger = BB("AMC", data["ohlcv"], 20, 2)

        # Check if we have enough data points to compute the indicators
        if len(sma_short) > 0 and len(sma_long) > 0 and len(rsi) > 0 and len(macd_line) > 0 and len(bollinger['upper']) > 0:
            # Momentum Trading Strategy
            if sma_short[-1] > sma_long[-1] and 30 < rsi[-1] < 70:
                amc_stake = 0.2  # 20% of the portfolio
                log("Momentum Buy Signal")
            
            # Mean Reversion Strategy
            elif data["ohlcv"][-1]["AMC"]["close"] < sma_long[-1] and rsi[-1] < 30:
                amc_stake = 0.2  # 20% of the portfolio
                log("Mean Reversion Buy Signal")

            # Breakout Strategy
            elif data["ohlcv"][-1]["AMC"]["close"] > bollinger['upper'][-1]:
                amc_stake = 0.2  # 20% of the portfolio
                log("Breakout Buy Signal")

            # Position Management - Sell condition based on SMA cross or RSI overbought
            elif sma_short[-1] < sma_long[-1] or rsi[-1] > 70:
                amc_stake = 0
                log("Sell Signal")

        # Adjust allocation based on strategy
        return TargetAllocation({"AMC": amc_stake})