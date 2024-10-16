#Linear Regression Telegram Trading Bot

##Overview

This project is a Telegram bot designed to help traders get real-time BTC price updates and trading signals based on a Linear Regression strategy. The bot integrates data from Binance's API to fetch live price information and stores it in a MongoDB database. It also uses technical analysis strategies, including a Linear Regression Channel and EMA18 calculation, to provide trading signals and daily trend analysis. Additionally, users can interact with the bot using commands, and the bot can send push notifications when certain trade conditions are met.

##Features

Real-Time BTC Price Fetching: The bot fetches the latest BTC price from Binance and stores it in MongoDB, making it easy to query and analyze.

Technical Analysis:

Linear Regression strategy that checks for buy and sell signals based on the price’s position relative to the regression channel.

EMA18 (Exponential Moving Average) for daily trend analysis.

Trading Signal Notifications: Automatically sends a notification when a buy or sell signal is triggered based on the strategy.

Scheduled Price Alerts: Sends regular price updates at specific times of the day.

Telegram Command Interactions: The bot offers various commands like /getprice, /start_push, /stop_push, and /dailytrend to give users control over how they interact with the price data.

##Project Structure

```
.
├── binance_api.py # Interacts with Binance API to fetch and store BTC price data in MongoDB
├── strategy.py # Implements the trading strategy (Linear Regression and EMA18)
├── main.py # Main entry point for running the bot, including testing API and DB connections
├── telegram_bot.py # Telegram bot implementation that handles commands and sends notifications
├── btc_1h.csv # Sample CSV data for historical BTC price in hourly intervals
├── test/ # Unit tests for binance_api, strategy, and telegram_bot functionalities
└── telegram_bot/ # Virtual environment-related files
```

Commands

Here are some of the commands you can use with the Telegram bot:

/start: Start the bot and interact with its features.

/greeting: Receive a friendly greeting from the bot.

/btcprice: Fetch the current BTC price from Binance.

/getprice: Get the latest BTC price from the MongoDB database.

/start_push: Start receiving hourly BTC price notifications.

/stop_push: Stop receiving BTC price notifications.

/dailytrend: Get the daily trend analysis based on the BTC price's position relative to the EMA18.

/list: Display a list of available commands.

How It Works

Fetching Price Data: The bot fetches the BTC price from Binance at regular intervals and stores it in MongoDB for further analysis.

Trading Strategy: The trading logic uses a Linear Regression strategy to detect price breakouts and trigger buy/sell signals. Additionally, the bot calculates the EMA18 to determine the trend (up, down, or sideways).

User Interactions: Users can start/stop price notifications and receive trading signals directly through Telegram commands.

Scheduling: The bot is set to send price data notifications at :59 of every hour and provide trend analysis based on daily price movements.

Setup and Installation

Clone the repository:

```
git clone <repository-url>
cd linear_regression_tg_bot
```

Install dependencies:

```
pip install -r requirements.txt
```

Set up your environment variables in a .env file:

```.env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
BINANCE_API_KEY=your-binance-api-key
BINANCE_API_SECRET=your-binance-api-secret
MONGO_URI=your-mongodb-uri
```

Run the bot locally:

```
python3 main.py
```

Deployment

To deploy this bot to Heroku, follow these steps:

Connect your GitHub repository to your Heroku account.

Set up environment variables in the Heroku settings (Telegram Bot Token, Binance API Key, etc.).

Deploy the app and make sure it's up and running.
