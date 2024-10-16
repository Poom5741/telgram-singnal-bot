import unittest
from binance_api import get_btc_price

class TestBinanceAPI(unittest.TestCase):
    def test_get_btc_price(self):
        """Test that the BTC price fetch returns a valid float or None."""
        price = get_btc_price()
        if price:
            self.assertTrue(isinstance(float(price), float))
        else:
            self.assertIsNone(price)

if __name__ == "__main__":
    unittest.main()
