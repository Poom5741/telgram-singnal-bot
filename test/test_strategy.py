import unittest
from strategy import LinearRegressionStrategy

class TestStrategy(unittest.TestCase):
    def setUp(self):
        # Set up the strategy with specific parameters
        self.strategy = LinearRegressionStrategy(window=5, sd_multiplier=0.4)

    def test_add_price(self):
        # Test adding prices
        self.strategy.add_price(50000)
        self.strategy.add_price(51000)
        self.strategy.add_price(52000)
        self.assertEqual(len(self.strategy.prices), 3)

    def test_check_signals(self):
        # Test checking signals
        prices = [50000, 50500, 51000, 52000, 53000]
        for price in prices:
            self.strategy.add_price(price)
        
        # Not enough data for signal initially
        signal = self.strategy.check_signals()
        self.assertIsNone(signal)

        # Add enough prices to trigger a signal
        self.strategy.add_price(54000)
        signal = self.strategy.check_signals()
        self.assertIn(signal, ["BUY", "SELL", None])  # Make sure signal is valid

if __name__ == '__main__':
    unittest.main()
