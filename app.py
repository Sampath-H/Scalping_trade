import streamlit as st
from strategy import generate_signals
from telegram_alerts import send_telegram_alert

st.set_page_config(page_title="MyScalperBot", layout="wide")

st.title("📊 MyScalperBot - Scalping Dashboard")
st.markdown("Use this dashboard to monitor NIFTY50 stocks and choose Auto/Manual trade mode.")

mode = st.radio("Select Mode", ["Auto", "Manual"], horizontal=True)
selected_stocks = st.multiselect("Select NIFTY50 Stocks", ["RELIANCE", "TCS", "INFY", "HDFC", "ICICIBANK", "SBIN", "KOTAKBANK"])
quantity = st.number_input("Enter Quantity per Trade", min_value=1, step=1)

if st.button("🔁 Scan Now"):
    if not selected_stocks:
        st.warning("Please select at least one stock.")
    else:
        signals = generate_signals(selected_stocks)
        for stock, signal in signals.items():
            st.write(f"📈 {stock}: {signal}")
            if mode == "Auto":
                send_telegram_alert(f"AUTO MODE: {stock} - {signal} (Qty: {quantity})")
            else:
                if st.button(f"✅ Approve Trade for {stock}"):
                    send_telegram_alert(f"MANUAL APPROVED: {stock} - {signal} (Qty: {quantity})")