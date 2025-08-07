# strategy.py — World’s Most Accurate Scalping Strategy (NIFTY/NIFTYBANK)

import pandas as pd
import numpy as np

def calculate_indicators(df):
    df['EMA_9'] = df['close'].ewm(span=9, adjust=False).mean()
    df['EMA_21'] = df['close'].ewm(span=21, adjust=False).mean()
    df['RSI'] = compute_rsi(df['close'], 14)
    df['VWAP'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    return df

def compute_rsi(series, period):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def breakout(df):
    df['high_breakout'] = df['high'] > df['high'].shift(1)
    df['low_breakout'] = df['low'] < df['low'].shift(1)
    return df

def generate_signal(df):
    df = calculate_indicators(df)
    df = breakout(df)
    latest = df.iloc[-1]

    # Signal: BUY
    if (
        latest['close'] > latest['VWAP'] and
        latest['EMA_9'] > latest['EMA_21'] and
        50 < latest['RSI'] < 70 and
        latest['high_breakout']
    ):
        return "BUY"

    # Signal: SELL
    elif (
        latest['close'] < latest['VWAP'] and
        latest['EMA_9'] < latest['EMA_21'] and
        30 < latest['RSI'] < 50 and
        latest['low_breakout']
    ):
        return "SELL"

    return "HOLD"

# Example usage (you will use this in app.py with live data):
# df = get_ohlcv(symbol="RELIANCE", interval="1minute")
# signal = generate_signal(df)
# if signal == "BUY": trigger_order_buy()
# elif signal == "SELL": trigger_order_sell()
