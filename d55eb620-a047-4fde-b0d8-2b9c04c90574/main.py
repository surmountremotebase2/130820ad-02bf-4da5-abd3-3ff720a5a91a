from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, SMA
from surmount.logging import log
from surmount.data import Asset, SocialSentiment

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "GME"
        # Assuming SocialSentiment takes symbol as parameter and returns sentiment analysis data
        self.data_list = [SocialSentiment(self.ticker)]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        sentiment_data = data[("social_sentiment", self.ticker)]
        current_sentiment_score = sentiment_data[-1]['twitterSentiment'] if sentiment_data else 0.5  # Neutral by default
        
        ohlcv_data = data["ohlcv"]
        macd_data = MACD(self.ticker, ohlcv_data, fast=12, slow=26)
        macd_line = macd_data['MACD'][-1] if macd_data['MACD'] else 0
        signal_line = macd_data['signal'][-1] if macd_data['signal'] else 0
        
        allocation = 0
        
        # Check for bullish momentum and positive sentiment
        if macd_line > signal line and current_sentiment_score > 0.6:
            log(f"Bullish Trend with Positive Sentiment for {self.ticker}")
            allocation = 1  # Full allocation
        
        # Check for bearish momentum or negative sentiment
        elif macd_line < signal_line or current_sentiment_score < 0.4:
            log(f"Bearish Trend or Negative Sentiment for {self.ticker}")
            allocation = 0  # No allocation
        
        return TargetAllocation({self.ticker: allocation})