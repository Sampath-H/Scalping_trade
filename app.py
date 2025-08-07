# app.py

import streamlit as st
from strategy import generate_entry_signal
import pandas as pd

st.set_page_config(page_title="MyScalperBot", layout="wide")
st.title("🔍 MyScalperBot – Scalping Strategy Dashboard")

uploaded_file = st.file_uploader("Upload market data CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if {"close", "vwap", "ema20", "volume", "avg_volume"}.issubset(df.columns):
        df["Signal"] = df.apply(generate_entry_signal, axis=1)
        st.dataframe(df[["close", "vwap", "ema20", "volume", "avg_volume", "Signal"]])
    else:
        st.error("Missing required columns in uploaded file.")
else:
    st.info("Please upload a CSV with market data.")
