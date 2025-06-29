import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from config import BINGX_API_KEY, BINGX_API_SECRET

class BingXClient:
    BASE_URL = "https://open-api.bingx.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"X-BX-APIKEY": BINGX_API_KEY})

    def _sign(self, params):
        query_string = urlencode(sorted(params.items()))
        signature = hmac.new(BINGX_API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params

    def get_positions(self):
        endpoint = "/openApi/swap/v2/user/positions"
        params = {"timestamp": int(time.time() * 1000)}
        signed_params = self._sign(params)
        response = self.session.get(self.BASE_URL + endpoint, params=signed_params)

        try:
            data = response.json()
        except Exception as e:
            print("❌ Failed to parse BingX response:", e)
            print("❌ Raw response text:", response.text)
            return {}

        positions = {}

        if data.get("code") == 0 and isinstance(data.get("data"), list):
            for pos in data["data"]:
                try:
                    symbol = pos["symbol"]
                    qty = float(pos["positionAmt"])
                    if qty != 0:
                        positions[symbol] = {
                            "positionSide": pos.get("positionSide", "UNKNOWN"),
                            "quantity": abs(qty)
                        }
                except Exception as e:
                    print(f"⚠️ Skipped invalid entry in BingX data: {pos} | Error: {e}")
        else:
            print("⚠️ Unexpected structure in BingX response:", data)

        return positions
