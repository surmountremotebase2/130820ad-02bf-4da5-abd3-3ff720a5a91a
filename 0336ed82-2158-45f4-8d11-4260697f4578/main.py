from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.ticker = "NVDA"
        self.entry_ema_length = 10  # Short-term EMA for entry signal
        self.exit_ema_length = 30  # Long-term EMA for exit signal
        self.profit_target = 1.10  # 10% profit target

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        # Returning a list with a single element as this strategy only trades NVDA
        return [self.ticker]

    def run(self, data):
        ohlcv = data["ohlcv"]
        nvda_data = ohlcv[self.ticker]
        
        # Check if we have enough data points for both EMAs
        if len(nvda_data) < max(self.entry_ema_length, self.exit_ema_length):
            return TargetAllocation({self.ticker: 0})
        
        # Calculate EMAs
        entry_ema = EMA(self.ticker, nvda_data, self.entry_ema_length)
        exit_ema = EMA(self.ticker, nvda_data, self.exit_ema_length)
        current_price = nvda_data[-1]['close']
        initial_buy_price = nvda_data[0]['close']  # Placeholder for buy price, you'd ideally store this after buying
        
        nvda_stake = 0  # Default to no position
        
        # Entry condition: current price moves above the short-term EMA (bullish signal)
        if current_price > entry_ema[-1]:
            log(f"Buying {self.ticker} at {current_price}, above EMA{self.entry_ema_length}")
            nvda_stake = 1  # Allocate 100% to NVDA
        
        # Exit conditions
        elif current_price < exit_ema[-1]:
            # Exit position if current price falls below the long-term EMA (potential downward trend)
            log(f"Selling {self.ticker} at {current_price}, below EMA{self.exit_ema_length}")
            nvda_stake = 0  # Sell off NVDA
        
        elif current_price >= initial_buy_price * self.profit_target:
            # Alternatively, exit position if a profit target of 10% has been reached
            log(f"Target reached: Selling {self.ticker} at {current_price}, {self.profit_target*100}% profit")
            nvda_stake = 0  # Sell off NVDA
            
        # Handling holding logic and other conditions should be considered based on account restrictions
        return TargetaAllocation({self.ticker: nvda_stake})