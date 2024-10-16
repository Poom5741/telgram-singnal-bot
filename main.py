import pandas as pd
from strategy import LinearRegressionStrategy
from telegram_bot import run_bot
from binance_api import fetch_btc_price, get_latest_price

# def test_strategy_with_csv():
#     """Test the linear regression strategy using btc_1h.csv data."""
#     # Load the CSV data
#     df = pd.read_csv('btc_1h.csv')
    
#     # Ensure that the Datetime column is properly parsed
#     df['Datetime'] = pd.to_datetime(df['Datetime'])
    
#     # Use 'Close' column as the price for the strategy
#     df['price'] = df['Close']
    
#     # Initialize the trading strategy
#     strategy = LinearRegressionStrategy(window=43, sd_multiplier=0.4)
    
#     # Add the prices to the strategy
#     for price in df['price']:
#         strategy.add_price(price)
    
#     # Check the signals
#     signal = strategy.check_signals()
#     if signal:
#         print(f"Strategy signal: {signal}")
#     else:
#         print("No signal generated from the strategy.")

# def test_ema18():
#     """Test the EMA18 trend logic using btc_1h.csv."""
#     df = pd.read_csv('btc_1h.csv')
    
#     # Ensure the 'Datetime' column is parsed and set the 'Close' price for the analysis
#     df['Datetime'] = pd.to_datetime(df['Datetime'])
#     df['price'] = df['Close']
    
#     # Calculate EMA18
#     df['EMA18'] = df['price'].ewm(span=18, adjust=False).mean()
    
#     # Get the latest data
#     latest_price = df['price'].iloc[-1]
#     ema18 = df['EMA18'].iloc[-1]
#     ema_slope = df['EMA18'].diff().iloc[-1]

#     print(f"Latest BTC Price: {latest_price}")
#     print(f"EMA18: {ema18}")
#     print(f"EMA Slope: {ema_slope}")

#     # Determine trend based on price and EMA18
#     if latest_price > ema18 and ema_slope > 15:
#         trend = "UP"
#     elif latest_price < ema18 and ema_slope < 15:
#         trend = "DOWN"
#     else:
#         trend = "SIDEWAYS"
    
#     print(f"Daily trend: {trend}")

def test_connections():
    """Test MongoDB and Binance API connections."""
    print("Testing Binance API...")
    btc_price = fetch_btc_price()
    if btc_price is not None:
        print(f"Binance API test successful. Fetched BTC price: {btc_price['price']}")
    else:
        print("Failed to fetch BTC price from Binance API.")
        return False

    print("Testing MongoDB connection...")
    latest_price = get_latest_price()
    if latest_price is not None:
        print(f"MongoDB test successful. Latest BTC price in DB: {latest_price['price']}")
    else:
        print("No price data found in MongoDB, or MongoDB connection failed.")
        return False

    return True

if __name__ == "__main__":
    # print("Testing strategy with CSV data...")
    # test_strategy_with_csv()
    
    # print("\nTesting EMA18 calculation...")
    # test_ema18()

    if test_connections():
        print("\nAll tests passed. Starting the bot...")
        run_bot()
    else:
        print("\nTests failed. Exiting...")
