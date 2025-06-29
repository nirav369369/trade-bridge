from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from binance_client import get_binance_positions, place_binance_order, sanitize_quantity
from bingx_client import get_bingx_positions

app = Flask(__name__)
CORS(app)

@app.route("/status")
def status():
    return jsonify({"status": "✅ Bridge is running successfully 🔁"})

@app.route("/positions")
def get_positions():
    try:
        binance_positions = get_binance_positions()
        bingx_positions = get_bingx_positions()

        return jsonify({
            "binance": binance_positions,
            "bingx": bingx_positions
        })
    except Exception as e:
        logging.error(f"Error fetching positions: {e}")
        return jsonify({"error": "Failed to fetch positions"}), 500

@app.route("/sync", methods=["POST"])
def sync_positions():
    try:
        bingx_positions = get_bingx_positions()
        binance_positions = get_binance_positions()

        sync_log = []

        for symbol, pos in bingx_positions.items():
            binance_symbol = symbol.replace("-", "")  # ADA-USDT -> ADAUSDT
            bingx_qty = sanitize_quantity(pos["quantity"])
            bingx_side = "BUY" if pos["positionSide"] == "LONG" else "SELL"

            binance_pos = binance_positions.get(binance_symbol)

            if not binance_pos:
                place_binance_order(binance_symbol, bingx_side, bingx_qty)
                sync_log.append(f"🆕 Placed order: {binance_symbol} {bingx_side} {bingx_qty}")
            else:
                sync_log.append(f"✅ Already open: {binance_symbol}")

        return jsonify({"message": "🔁 Sync complete", "details": sync_log})
    except Exception as e:
        logging.error(f"❌ Sync failed: {e}")
        return jsonify({"error": "Sync failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)