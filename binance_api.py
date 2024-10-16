from binance.client import Client
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd
import certifi  # Added certifi for SSL certificates

load_dotenv()

# Initialize Binance and MongoDB clients
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
binance_client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# MongoDB connection with SSL certificate verification
MONGO_URI = os.getenv('MONGO_URI')
mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())  # Using certifi to handle SSL
db = mongo_client['trading_data']
price_collection = db['btc_price_data']

def fetch_btc_price():
    """Fetch the latest 1-hour BTC price from Binance and store it in MongoDB."""
    try:
        ticker = binance_client.get_symbol_ticker(symbol="BTCUSDT")
        price_data = {
            "symbol": ticker['symbol'],
            "price": float(ticker['price']),
            "timestamp": pd.Timestamp.utcnow()
        }
        print(f"Fetched BTC Price: {price_data}")  # Print price data for verification
        price_collection.insert_one(price_data)
        return price_data
    except Exception as e:
        print(f"Error fetching BTC price: {e}")
        return None


def get_latest_price():
    """Retrieve the latest BTC price from MongoDB."""
    try:
        result = list(price_collection.find().sort("timestamp", -1).limit(1))
        if not result:
            print("No price data available in the database.")
            return None
        print(f"Latest price data from MongoDB: {result[0]}")  # Print to verify
        return result[0]
    except Exception as e:
        print(f"Error fetching the latest price from MongoDB: {e}")
        return None


def get_all_prices():
    """Retrieve all stored BTC prices from MongoDB."""
    return pd.DataFrame(list(price_collection.find().sort("timestamp", -1)))
