import logging
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, JobQueue
from binance_api import fetch_btc_price, get_latest_price, get_all_prices
from strategy import LinearRegressionStrategy
from dotenv import load_dotenv
import os
import datetime

# Load environment variables
load_dotenv()

# Fetch token from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Initialize the trading strategy
strategy = LinearRegressionStrategy(window=43, sd_multiplier=0.4)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Send Greeting", callback_data='send_greeting')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Click the button to get a greeting message:", reply_markup=reply_markup)

# Define the /greeting command handler
async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Nice to meet you!")

# Function to fetch BTC price, store in DB, and trigger notifications if a signal occurs
async def scheduled_fetch_and_signal(context: ContextTypes.DEFAULT_TYPE):
    """Fetches BTC price and checks for trading signals every hour."""
    price = fetch_btc_price()
    
    if price:
        # Add price to the strategy
        strategy.add_price(price['price'])
        signal = strategy.check_signals()
        
        # Notify user only if a trading signal is triggered
        if signal == "BUY":
            await context.bot.send_message(chat_id=context.job.chat_id, text=f"BUY signal triggered at BTC price: ${price['price']}")
        elif signal == "SELL":
            await context.bot.send_message(chat_id=context.job.chat_id, text=f"SELL signal triggered at BTC price: ${price['price']}")
        else:
            # Silent data store; no notification for no signal
            logging.info(f"No trading signal at ${price['price']}. Data stored.")
    else:
        logging.error("Could not fetch the BTC price.")

# Start fetching and writing price data to the database every hour automatically
def start_auto_fetch_and_store(job_queue: JobQueue):
    """Starts a job that fetches and writes BTC price to the database every hour."""
    job_queue.run_repeating(scheduled_fetch_and_signal, interval=3600, first=0)  # Run every hour (3600 seconds)

# Add a command to start notifications
async def start_push_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the push notification for BTC price with trading signals."""
    chat_id = update.message.chat_id
    job_queue = context.job_queue

    # Schedule the job to run every hour
    job_queue.run_repeating(scheduled_fetch_and_signal, interval=3600, first=0, chat_id=chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Started BTC price fetching every hour with trading signal notifications!")

# Add a command to stop notifications
async def stop_push_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop the push notifications."""
    chat_id = update.message.chat_id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    
    if not current_jobs:
        await update.message.reply_text("No active notifications found.")
        return

    for job in current_jobs:
        job.schedule_removal()

    await update.message.reply_text("Stopped BTC price notifications.")

# Command to get the latest BTC price from the database
async def get_latest_price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /getprice command and send the latest BTC price to the user."""
    latest_price_data = get_latest_price()
    
    if latest_price_data is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No price data available in the database.")
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"The latest BTC price is: ${latest_price_data['price']} (as of {latest_price_data['timestamp']})"
        )

# Function to handle /dailyTrend command using EMA18 and determine daily trend
async def daily_trend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provide daily trend based on EMA18 from the database."""
    try:
        # Fetch all stored prices from the database
        all_prices_df = get_all_prices()

        if all_prices_df.empty:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No data available to calculate the daily trend.")
            return

        # Calculate EMA18
        all_prices_df['EMA18'] = all_prices_df['price'].ewm(span=18, adjust=False).mean()
        latest_price = all_prices_df['price'].iloc[-1]
        ema18 = all_prices_df['EMA18'].iloc[-1]
        ema_slope = all_prices_df['EMA18'].diff().iloc[-1]

        # Determine trend based on price vs. EMA18 and slope of EMA18
        if latest_price > ema18 and ema_slope > 15:
            trend = "UP"
        elif latest_price < ema18 and ema_slope < 15:
            trend = "DOWN"
        else:
            trend = "SIDEWAYS"

        # Send daily trend information
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Today's BTC Price: ${latest_price:.2f}\n"
                 f"EMA18: ${ema18:.2f}\n"
                 f"Trend: {trend}"
        )

    except Exception as e:
        logging.error(f"Error calculating daily trend: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error calculating daily trend.")

# Command to list all available commands
async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /list command and show all available bot commands."""
    commands = [
        "/start - Start the bot and interact with buttons",
        "/greeting - Get a greeting from the bot",
        "/btcprice - Fetch and display the current BTC price",
        "/getprice - Get the latest BTC price from the database",
        "/start_push - Start hourly notifications for BTC price",
        "/stop_push - Stop BTC price notifications",
        "/dailyTrend - Get the daily trend based on EMA18",
        "/list - List all available commands"
    ]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(commands))

# Callback function for button clicks
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'send_greeting':
        await query.edit_message_text(f"Hello, {update.effective_user.first_name}! Nice to meet you!")

# Main function to set up the bot
def run_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add the /start, /greeting, /btcprice, /getprice command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('greeting', greeting))
    application.add_handler(CommandHandler('btcprice', btc_price))
    application.add_handler(CommandHandler('getprice', get_latest_price_command))

    # Add command to list all available commands
    application.add_handler(CommandHandler('list', list_commands))

    # Add command for daily trend
    application.add_handler(CommandHandler('dailyTrend', daily_trend))

    # Add command to start/stop push notifications
    application.add_handler(CommandHandler('start_push', start_push_notification))
    application.add_handler(CommandHandler('stop_push', stop_push_notification))

    # Add callback handler for button interaction
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start fetching BTC price data every hour (this happens quietly)
    start_auto_fetch_and_store(application.job_queue)

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    run_bot()
