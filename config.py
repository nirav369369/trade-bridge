# config.py

# ✅ Binance API Keys
BINANCE_API_KEY = "Ufbg9TKjd0Z3GG6I82zhE26x9WDU83pXCdwxKCR0BNHXm8wAY5BBlbYckS2eR2Ya"
BINANCE_API_SECRET = "e5giUNSU1JBvvfwM5UmkNUsepJ7u4ZGAAuW8HfUHHKvhRCekq2l09hUYM5F3kYLy"

# ✅ BingX API Keys
BINGX_API_KEY = "NortAFqrEbvmrdHmG3B3x8RZ716KuhBqOydjOvZgy5252w3zg0eUDXzMErdpvcHjYDvAcVxyI2i7hiKiO2oA"
BINGX_API_SECRET = "Sr86wOsMlbgkFmDimBcOVkzXjLKEbggeKZoYQBvM7V6M6wLhXkvGoSDkVxaZDYMLv0cLu42dpaf5r1vhLAFg"

# ✅ Binance Symbol Mapping (no dashes)
BINANCE_SYMBOL_MAP = {
    "BTC-USDT": "BTCUSDT",
    "ETH-USDT": "ETHUSDT",
    "SOL-USDT": "SOLUSDT",
    "XRP-USDT": "XRPUSDT",
    "AAVE-USDT": "AAVEUSDT",
    "LTC-USDT": "LTCUSDT",
    "UNI-USDT": "UNIUSDT",
    "BNB-USDT": "BNBUSDT",
    "ADA-USDT": "ADAUSDT",
    "BCH-USDT": "BCHUSDT",
    "LINK-USDT": "LINKUSDT",
    "APT-USDT": "APTUSDT",
    "NEAR-USDT": "NEARUSDT",
    "DOT-USDT": "DOTUSDT",
    "ETC-USDT": "ETCUSDT",
}

# ✅ Bridge Settings
LOOP_INTERVAL = 10  # seconds between each sync
DEFAULT_LEVERAGE = 5  # leverage to apply on Binance
TRADE_SIZE_MULTIPLIER = 1.0  # adjust this to copy partial (e.g. 0.5) or extra (e.g. 2.0) position size