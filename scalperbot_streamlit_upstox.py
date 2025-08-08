
import streamlit as st
import pandas as pd
from strategy import generate_signals  # This imports your logic from strategy.py
from upstox_api.api import Upstox, Session
from telegram_alerts import send_telegram_message

st.set_page_config(page_title="MyScalperBot", layout="wide")

st.title("📈 MyScalperBot - Real-Time Scalping Signals")

st.sidebar.header("🔧 Configuration")
api_key = st.sidebar.text_input("Upstox API Key", type="password")
api_secret = st.sidebar.text_input("Upstox API Secret", type="password")
redirect_uri = st.sidebar.text_input("Redirect URI")
access_token = st.sidebar.text_input("Access Token", type="password")
telegram_enabled = st.sidebar.checkbox("Enable Telegram Alerts")
mode = st.sidebar.radio("Trade Mode", ["Manual", "Auto"])
quantity = st.sidebar.number_input("Trade Quantity", min_value=1, value=15)
symbols_csv = st.sidebar.file_uploader("Upload NIFTY50 Symbols CSV", type=["csv"])

if symbols_csv is not None:
    df_symbols = pd.read_csv(symbols_csv)
    selected_symbols = st.sidebar.multiselect("Select Symbols to Monitor", df_symbols["symbol"].tolist())
else:
    st.warning("Please upload your NIFTY50 symbols CSV file.")

if st.button("Start Scanning") and symbols_csv is not None:
    st.success("Scanning started...")
    result_df = generate_signals(selected_symbols)
    st.dataframe(result_df)

    if telegram_enabled:
        for _, row in result_df.iterrows():
            message = f"Signal: {row['Signal']} | {row['Symbol']} @ {row['Close']}"
            send_telegram_message(message)
