import logging
import time
from binance_client import BinanceClient
from bingx_client import BingXClient
from binance_symbol_rules import adjust_quantity

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize API clients
binance = BinanceClient()
bingx = BingXClient()

# Symbol mapping: BingX symbol => Binance symbol
SYMBOL_MAP = {
    'BTC-USDT': 'BTCUSDT',
    'ETH-USDT': 'ETHUSDT',
    'BNB-USDT': 'BNBUSDT',
    'SOL-USDT': 'SOLUSDT',
    'ADA-USDT': 'ADAUSDT',
    'DOT-USDT': 'DOTUSDT',
    'ONDO-USDT': 'ONDOUSDT'
}

# Retry mechanism
retry_tracker = {}
MAX_RETRIES = 3
RETRY_DELAY = 300  # seconds

def can_retry(symbol):
    retry_data = retry_tracker.get(symbol)
    if not retry_data:
        return True
    if retry_data['count'] >= MAX_RETRIES:
        if time.time() - retry_data['last_attempt'] > RETRY_DELAY:
            retry_tracker[symbol] = {'count': 0, 'last_attempt': 0}
            return True
        return False
    return True

def record_retry(symbol):
    data = retry_tracker.get(symbol, {'count': 0, 'last_attempt': 0})
    data['count'] += 1
    data['last_attempt'] = time.time()
    retry_tracker[symbol] = data

def main():
    while True:
        try:
            # Step 1: Fetch positions
            bingx_positions = bingx.get_positions()
            binance_positions = binance.get_positions()

            logging.info("🔍 Raw BingX Positions: %s", bingx_positions)
            logging.info("🔍 Raw Binance Positions: %s", binance_positions)

            # Step 2: Validate and convert to dict
            if isinstance(bingx_positions, list) and all(isinstance(p, dict) for p in bingx_positions):
                bingx_positions = {p['symbol']: p for p in bingx_positions}
            else:
                logging.error("❌ Unexpected format in bingx_positions: %s", bingx_positions)
                time.sleep(5)
                continue

            if isinstance(binance_positions, list) and all(isinstance(p, dict) for p in binance_positions):
                binance_positions = {p['symbol']: p for p in binance_positions}
            else:
                logging.error("❌ Unexpected format in binance_positions: %s", binance_positions)
                time.sleep(5)
                continue

            # Step 3: Sync positions
            for bingx_symbol, bingx_pos in bingx_positions.items():
                binance_symbol = SYMBOL_MAP.get(bingx_symbol)
                if not binance_symbol:
                    logging.warning("⚠️ Symbol not mapped: %s", bingx_symbol)
                    continue

                desired_qty = float(bingx_pos.get("quantity", 0))
                current_qty = float(binance_positions.get(binance_symbol, {}).get("quantity", 0))
                delta = round(desired_qty - current_qty, 8)

                if abs(delta) < 0.001:
                    continue  # No action needed

                side = "BUY" if delta > 0 else "SELL"
                qty = abs(delta)
                adjusted_qty = adjust_quantity(binance_symbol, qty)

                price = binance.get_price(binance_symbol)
                notional = float(price) * adjusted_qty
                if notional < 5:
                    logging.warning("❌ Notional < 5 USDT: %s (qty: %s @ %s)", notional, adjusted_qty, price)
                    continue

                if not can_retry(binance_symbol):
                    logging.info("⏸ Skipping %s due to retry limit.", binance_symbol)
                    continue

                logging.info("✅ Placing order: %s %s Qty: %s", binance_symbol, side, adjusted_qty)
                response = binance.place_market_order(binance_symbol, side, adjusted_qty)
                logging.info("🧾 Order response: %s", response)

                if isinstance(response, dict) and response.get("code") == -2019:
                    record_retry(binance_symbol)

        except Exception as e:
            logging.error("🔥 Error in bridge loop: %s", e)

        time.sleep(5)

if __name__ == "__main__":
    main()
