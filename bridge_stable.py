bridge_stable.py (Main Script)

import logging import time from binance_client import BinanceClient from bingx_client import BingXClient from binance_symbol_rules import adjust_quantity

logging.basicConfig(level=logging.INFO)

Initialize clients

binance = BinanceClient() bingx = BingXClient()

Symbol mapping: BingX symbol => Binance symbol

SYMBOL_MAP = { 'BTC-USDT': 'BTCUSDT', 'ETH-USDT': 'ETHUSDT', 'BNB-USDT': 'BNBUSDT', 'SOL-USDT': 'SOLUSDT', 'ADA-USDT': 'ADAUSDT', 'DOT-USDT': 'DOTUSDT', 'ONDO-USDT': 'ONDOUSDT' }

retry_tracker = {} MAX_RETRIES = 3 RETRY_DELAY = 300

def can_retry(symbol): retry_data = retry_tracker.get(symbol) if not retry_data: return True if retry_data['count'] >= MAX_RETRIES: if time.time() - retry_data['last_attempt'] > RETRY_DELAY: retry_tracker[symbol] = {'count': 0, 'last_attempt': 0} return True return False return True

def record_retry(symbol): data = retry_tracker.get(symbol, {'count': 0, 'last_attempt': 0}) data['count'] += 1 data['last_attempt'] = time.time() retry_tracker[symbol] = data

def main(): while True: try: bingx_positions = bingx.get_positions() binance_positions = binance.get_positions()

if not isinstance(bingx_positions, dict):
            logging.error("❌ BingX returned invalid format: %s", bingx_positions)
            time.sleep(5)
            continue

        if not isinstance(binance_positions, dict):
            logging.error("❌ Binance returned invalid format: %s", binance_positions)
            time.sleep(5)
            continue

        logging.info("📊 Binance Positions: %s", binance_positions)
        logging.info("📊 BingX Positions: %s", bingx_positions)

        for bingx_symbol, bingx_pos in bingx_positions.items():
            binance_symbol = SYMBOL_MAP.get(bingx_symbol)
            if not binance_symbol:
                logging.warning("❌ Symbol not mapped: %s", bingx_symbol)
                continue

            desired_qty = float(bingx_pos["quantity"])
            current_binance_qty = float(binance_positions.get(binance_symbol, {}).get("quantity", 0))
            delta = round(desired_qty - current_binance_qty, 8)

            if abs(delta) < 0.001:
                continue

            side = "BUY" if delta > 0 else "SELL"
            qty = abs(delta)
            adjusted_qty = adjust_quantity(binance_symbol, qty)

            price = binance.get_price(binance_symbol)
            notional = float(price) * adjusted_qty
            if notional < 5:
                logging.warning("❌ Order notional < 5 USDT: %s (qty: %s @ price: %s)", notional, adjusted_qty, price)
                continue

            if not can_retry(binance_symbol):
                logging.info("⏸ Skipping %s due to recent margin errors.", binance_symbol)
                continue

            logging.info("✅ Mirroring => %s | %s | Qty: %s", binance_symbol, side, adjusted_qty)
            response = binance.place_market_order(binance_symbol, side, adjusted_qty)
            logging.info("🧾 Order response: %s", response)

            if isinstance(response, dict) and response.get('code') == -2019:
                record_retry(binance_symbol)

    except Exception as e:
        logging.error("🔥 Error in bridge loop: %s", e)

    time.sleep(5)

if name == "main": main()
