import streamlit as st
import yfinance as yf
import pandas as pd

def fetch_price_data(tickers, start, end):
    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        threads=False
    )

    st.write("Raw data:")
    st.write(data.head())
    st.write("Columns:", data.columns)

    if data.empty:
        return pd.DataFrame()

    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    elif "Close" in data.columns:
        prices = data[["Close"]]
    else:
        return pd.DataFrame()

    return prices.dropna(how="all")

def calculate_returns(price_df):
    return price_df.pct_change().dropna()
