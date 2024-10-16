import numpy as np
import pandas as pd
from scipy.stats import linregress

class LinearRegressionStrategy:
    def __init__(self, window=43, sd_multiplier=0.4):
        """
        Initialize the strategy with a window size and standard deviation multiplier.
        :param window: The lookback window for the linear regression (default is 43).
        :param sd_multiplier: The standard deviation multiplier for the channel (default is 0.4).
        """
        self.window = window
        self.sd_multiplier = sd_multiplier
        self.prices = []

    def add_price(self, price):
        """
        Add a new price to the series and remove the oldest price if the series exceeds the window length.
        :param price: New price to be added.
        """
        self.prices.append(price)
        if len(self.prices) > self.window:
            self.prices.pop(0)

    def calculate_regression_channels(self):
        """
        Calculate the regression line, upper and lower channels based on the current price data.
        :return: A tuple containing the regression line, upper channel, and lower channel.
        """
        y = np.array(self.prices)
        x = np.arange(len(y))
        slope, intercept, _, _, _ = linregress(x, y)

        regression_line = intercept + slope * x[-1]
        std_dev = np.std(y)
        upper_channel = regression_line + self.sd_multiplier * std_dev
        lower_channel = regression_line - self.sd_multiplier * std_dev

        return regression_line, upper_channel, lower_channel

    def check_signals(self):
        """
        Check for a buy or sell signal based on the current price and calculated regression channels.
        :return: "BUY" if price crosses above the upper channel, "SELL" if price crosses below the lower channel, 
                 None if no signal.
        """
        if len(self.prices) < self.window:
            return None

        regression_line, upper_channel, lower_channel = self.calculate_regression_channels()
        current_price = self.prices[-1]

        if current_price > upper_channel:
            return "BUY"
        elif current_price < lower_channel:
            return "SELL"
        return None

    def apply_to_historical_data(self, price_data):
        """
        Apply the trading strategy to a historical price dataset.
        :param price_data: A pandas DataFrame containing price data.
        :return: A pandas DataFrame with the buy/sell signals appended.
        """
        price_data['signal'] = None

        for i in range(len(price_data)):
            self.add_price(price_data['Close'].iloc[i])
            signal = self.check_signals()
            price_data['signal'].iloc[i] = signal

        return price_data
