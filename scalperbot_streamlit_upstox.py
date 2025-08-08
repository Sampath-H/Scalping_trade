import streamlit as st
import pandas as pd
import time
from strategy import generate_signals
from upstox_integration import place_order, get_upstox_instance
from telegram_alerts import send_telegram_alert

# API Credentials (SECURELY INTEGRATED)
UPSTOX_API_KEY = "55b2f37e-xxx"
UPSTOX_API_SECRET = "48e1445e-xxx"
UPSTOX_REDIRECT_URI = "https://127.0.0.1"
UPSTOX_ACCESS_TOKEN = "1.eyJraWQiOiIxZEdIZ1ZLTjNPZ0..."
UPSTOX_CLIENT_ID = "z9sry1v7lq-xxx"

TELEGRAM_BOT_TOKEN = "6635869994:AAGNLxiE7XgE1s9UTU0xxx"
TELEGRAM_CHAT_ID = "1042202004"

st.set_page_config(page_title="ScalperBot Streamlit App", layout="wide")
st.title("🤖 ScalperBot with Upstox Integration")

stocks = [
    "RELIANCE", "TCS", "INFY", "ICICIBANK", "HDFCBANK", "SBIN", "AXISBANK", "KOTAKBANK",
    "ITC", "LT", "BHARTIARTL", "ASIANPAINT", "MARUTI", "BAJAJFINSV", "BAJFINANCE", "HINDUNILVR",
    "POWERGRID", "TITAN", "ULTRACEMCO", "WIPRO"
]

selected_stocks = st.multiselect("Select stocks to monitor:", stocks)
auto_mode = st.toggle("Auto Mode (Place orders automatically)")
trade_quantity = st.number_input("Trade Quantity", min_value=1, value=1)

if "previous_signals" not in st.session_state:
    st.session_state.previous_signals = {}

upstox = get_upstox_instance()

placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader("📊 Live Trading Signals")
        all_data = []

        for stock in selected_stocks:
            signal = generate_signals(stock)
            prev_signal = st.session_state.previous_signals.get(stock)

            if signal != prev_signal and signal != "HOLD":
                st.session_state.previous_signals[stock] = signal
                send_telegram_alert(f"{stock} signal: {signal}")

                if auto_mode:
                    side = "BUY" if signal == "BUY" else "SELL"
                    try:
                        place_order(upstox, stock, side, trade_quantity)
                        send_telegram_alert(f"Order Placed: {side} {stock} x {trade_quantity}")
                    except Exception as e:
                        send_telegram_alert(f"Order Failed for {stock}: {str(e)}")

            all_data.append({"Stock": stock, "Signal": signal})

        st.dataframe(pd.DataFrame(all_data))
        time.sleep(15)
