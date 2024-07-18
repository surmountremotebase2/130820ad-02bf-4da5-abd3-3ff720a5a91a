import yfinance as yf
import time
from datetime import datetime, timedelta

# Constants
TICKER = 'SOUN'
INVESTMENT = 100
PROFIT_TARGET = 10

# Function to get the current stock price
def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    todays_data = stock.history(period='1d')
    return todays_data['Close'][0]

# Function to calculate the profit based on the current price
def calculate_profit(buy_price, current_price, investment):
    shares = investment / buy_price
    current_value = shares * current_price
    return current_value - investment

# Simulated trading function
def trade_sound_ai():
    buy_price = get_current_price(TICKER)
    print(f"Bought {TICKER} at {buy_price:.2f}")

    while True:
        current_price = get_current_price(TICKER)
        profit = calculate_profit(buy_price, current_price, INVESTMENT)
        print(f"Current price of {TICKER} is {current_price:.2f}. Profit: ${profit:.2f}")

        if profit >= PROFIT_TARGET:
            print(f"Profit target reached! Selling {TICKER} at {current_price:.2f} for a profit of ${profit:.2f}")
            # Here you would implement the sell logic
            break

        # Sleep to avoid hitting the API rate limit
        time.sleep(60)  # Check the price every minute

if __name__ == "__main__":
    trade_sound_ai()