# config.py

# ✅ Binance API Keys
BINANCE_API_KEY = "your_key"
BINANCE_API_SECRET = "your_key"

# ✅ BingX API Keys
BINGX_API_KEY = "your_key"
BINGX_API_SECRET = "your_key"

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
