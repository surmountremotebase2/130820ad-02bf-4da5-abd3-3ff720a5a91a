from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import Momentum, SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets you're interested in.
        self.tickers = ["AAPL", "MSFT", "TSLA", "AMZN"]
        # This list would ideally be developed based on research to identify stocks with high and predictable volatility that leads to profitable options trading.
        self.lookback_days = 30  # Lookback period for momentum and simple moving average calculations.

    @property
    def interval(self):
        # Daily data to avoid pattern day trading
        return "1day"

    @property
    def assets(self):
        return self.tickers
    
    def run(self, data):
        best_option_call_put_allocation = {}
        highest_momentum = 0
        selected_stock = None
        
        # Loop through tickers to calculate momentum and identify the stock with the highest positive or negative momentum
        for ticker in self.tickets:
            momentum_values = Momentum(ticker, data["ohlcv"], self.lookback_days)
            
            if momentum_values is not None and abs(momentum_values[-1]) > highest_momentum:
                highest_momentum = abs(momentum_values[-1])
                selected_stock = ticker
        
        if selected_stock is None:
            log("No suitable stock found for options trading.")
            return TargetAllocation({})
        
        # Determine trend direction for the stock with the highest momentum to decide on call or put
        sma_short = SMA(selected_stock, data["ohlcv"], int(self.lookback_days / 2))[-1]
        sma_long = SMA(selected_stock, data["ohlcv"], self.lookback_days)[-1]
        
        if sma_short > sma_long:
            log(f"Buying call options for {selected_stock} based on positive momentum and uptrend.")
            best_option_call_put_allocation[selected_stock] = 1  # Simulating a buy call operation; in practice, you would need to adjust based on options specifics.
        else:
            log(f"Buying put options for {selected_stock} based on negative momentum and downtrend.")
            best_option_call_put_allocation[selected_stock] = -1 # Simulating a buy put operation; adjust based on your options strategy specifics.
        
        return TargetAllocation(best_option_call_put_allocation)