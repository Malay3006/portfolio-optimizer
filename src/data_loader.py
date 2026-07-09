import yfinance as yf
import pandas as pd


def fetch_price_data(tickers, start, end):
    """Fetch adjusted close prices for given tickers between start and end dates."""
    data = yf.download(
    tickers,
    start=start,
    end=end,
    auto_adjust=True,
    progress=False,
    threads=False
    )["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame()
    return data.dropna()


def calculate_returns(price_df):
    """Calculate daily percentage returns from price data."""
    return price_df.pct_change().dropna()
