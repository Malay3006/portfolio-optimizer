import yfinance as yf
import pandas as pd

def fetch_price_data(tickers, start, end):
    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        threads=False
    )

    if data.empty:
        return pd.DataFrame()

    if "Close" in data.columns:
        prices = data["Close"]
    else:
        prices = data

    if isinstance(prices, pd.Series):
        prices = prices.to_frame()

    return prices.dropna()

def calculate_returns(price_df):
    return price_df.pct_change().dropna()
