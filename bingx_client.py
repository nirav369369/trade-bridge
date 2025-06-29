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
        data = response.json()

        positions = {}
        if data.get("code") == 0:
            for pos in data.get("data", []):
                symbol = pos.get("symbol")
                qty = float(pos.get("positionAmt", 0))
                if qty != 0:
                    positions[symbol] = {
                        "quantity": abs(qty),
                        "positionSide": pos.get("positionSide", "BOTH")
                    }
        return positions
