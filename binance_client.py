import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from config import BINANCE_API_KEY, BINANCE_API_SECRET

class BinanceClient:
    BASE_URL = "https://fapi.binance.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": BINANCE_API_KEY})

    def _sign(self, params):
        query_string = urlencode(params)
        signature = hmac.new(BINANCE_API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params

    def get_positions(self):
        endpoint = "/fapi/v2/positionRisk"
        params = {"timestamp": int(time.time() * 1000)}
        signed_params = self._sign(params)
        response = self.session.get(self.BASE_URL + endpoint, params=signed_params)
        
        try:
            data = response.json()
        except Exception as e:
            print("❌ Failed to parse Binance positions:", e)
            print("❌ Raw response text:", response.text)
            return {}

        positions = {}
        if isinstance(data, list):
            for pos in data:
                try:
                    symbol = pos["symbol"]
                    qty = float(pos["positionAmt"])
                    if qty != 0:
                        positions[symbol] = {
                            "positionSide": pos.get("positionSide", "UNKNOWN"),
                            "quantity": abs(qty)
                        }
                except Exception as e:
                    print(f"⚠️ Skipped invalid Binance position: {pos} | Error: {e}")
        else:
            print("⚠️ Unexpected Binance response structure:", data)

        return positions

    def get_account_info(self):
        endpoint = "/fapi/v2/account"
        params = {"timestamp": int(time.time() * 1000)}
        signed_params = self._sign(params)
        response = self.session.get(self.BASE_URL + endpoint, params=signed_params)
        return response.json()

    def get_price(self, symbol):
        endpoint = "/fapi/v1/premiumIndex"
        params = {"symbol": symbol}
        response = self.session.get(self.BASE_URL + endpoint, params=params)
        return float(response.json()["markPrice"])

    def place_market_order(self, symbol, side, quantity):
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }
        signed_params = self._sign(params)
        response = self.session.post(self.BASE_URL + endpoint, params=signed_params)
        return response.json()
