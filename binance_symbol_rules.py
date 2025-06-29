import requests
import logging

# Dictionary to store symbol and its step size
symbol_rules = {}

def load_symbol_rules():
    """
    Fetch symbol rules from Binance API and store step sizes.
    """
    global symbol_rules
    try:
        url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "symbols" not in data:
            logging.error("❌ Binance response missing 'symbols': %s", data)
            return

        for symbol_info in data["symbols"]:
            symbol = symbol_info["symbol"]
            for filt in symbol_info["filters"]:
                if filt["filterType"] == "LOT_SIZE":
                    step_size = float(filt["stepSize"])
                    symbol_rules[symbol] = step_size

    except requests.exceptions.RequestException as e:
        logging.error("❌ Network error while loading symbol rules: %s", e)
    except Exception as e:
        logging.error("❌ Unexpected error in load_symbol_rules(): %s", e)

def adjust_quantity(symbol, quantity):
    """
    Adjust the quantity based on Binance's stepSize rules.
    """
    if symbol not in symbol_rules:
        load_symbol_rules()

    step_size = symbol_rules.get(symbol, 1.0)
    precision = len(str(step_size).split('.')[-1].rstrip('0'))  # Handle 0.001000 case
    adjusted_qty = round(quantity / step_size) * step_size
    return round(adjusted_qty, precision)
