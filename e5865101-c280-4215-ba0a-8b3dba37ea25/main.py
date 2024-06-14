from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        # Sample list of AI stocks (This would normally come from a dynamic source or comprehensive list)
        self.tickers = ["AIPL", "DEEP", "NEURAL", "LEARN"]
        
        # Assuming these are pre-filtered AI stocks for simplification
        self.ai_stocks = self.tickers

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        # focuses on the AI stocks only
        return self.ai_stocks

    @property
    def data(self):
        # We need OHLCV data to calculate SMAs and check current prices
        return [OHLCV(ticker) for ticker in self.ai_stocks]

    def run(self, data):
        allocation_dict = {}
        
        for ticker in self.ai_stocks:
            ohlcv_data = data["ohlcv"][ticker]
            current_price = ohlcv_data[-1]['close']
            
            # Checking if the latest price is under $1
            if current  <= 1.00:
                sma_20 = SMA(ticker, ohlcv_data, 20)
                
                # Assuming the moving average could be None if data is insufficient
                if sma_20 is not None and len(sma_20) > 0:
                    avg_20 = sma_20[-1]
                    
                    if current_price > avg_20:
                        # Stock is below $1 and above its 20-day SMA, indicating potential
                        allocation_dict[ticker] = 1.0 / len(self.ai_stocks)
                    else:
                        allocation_dict[ticker] = 0
                else:
                    allocation_dict[ticker] = 0
            else:
                allocation_dict[ticker] = 0
                
        return TargetAllocation(allocation_dict)