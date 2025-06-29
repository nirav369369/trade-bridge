import requests

symbol_rules = {}

def load_symbol_rules():
    global symbol_rules
    url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
    response = requests.get(url)
    data = response.json()

    for symbol_info in data['symbols']:
        symbol = symbol_info['symbol']
        for f in symbol_info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_size = float(f['stepSize'])
                symbol_rules[symbol] = step_size

def adjust_quantity(symbol, quantity):
    if symbol not in symbol_rules:
        load_symbol_rules()

    step_size = symbol_rules.get(symbol, 1.0)

    precision = abs(f"{step_size:.10f}".find('1') - 1)
    adjusted_qty = round(quantity, precision)
    return adjusted_qty