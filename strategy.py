
# strategy.py

def generate_entry_signal(data):
    # Entry: Price above VWAP and 20 EMA, with volume confirmation
    price = data["close"]
    vwap = data["vwap"]
    ema20 = data["ema20"]
    volume = data["volume"]
    avg_volume = data["avg_volume"]

    if price > vwap and price > ema20 and volume > avg_volume * 1.2:
        return "BUY"
    elif price < vwap and price < ema20 and volume > avg_volume * 1.2:
        return "SELL"
    else:
        return "HOLD"

def get_stoploss(entry_price, direction, atr):
    # Initial stoploss based on ATR
    sl_buffer = atr * 1.2
    return entry_price - sl_buffer if direction == "BUY" else entry_price + sl_buffer

def get_trailing_sl(current_price, direction, atr, last_sl):
    # Trailing SL: lock in profit as price moves
    trail_buffer = atr * 1.2
    if direction == "BUY":
        new_sl = max(last_sl, current_price - trail_buffer)
    else:
        new_sl = min(last_sl, current_price + trail_buffer)
    return new_sl
