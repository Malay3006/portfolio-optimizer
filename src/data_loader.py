import yfinance as yf
import pandas as pd

def fetch_price_data(tickers, start, end):
    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        threads=False
    )

    if data.empty:
        return pd.DataFrame()

    # MultiIndex columns handle karo
    if isinstance(data.columns, pd.MultiIndex):
        if "Adj Close" in data.columns.get_level_values(0):
            prices = data["Adj Close"]
        else:
            prices = data["Close"]
    else:
        if "Adj Close" in data.columns:
            prices = data[["Adj Close"]]
        else:
            prices = data[["Close"]]

    return prices.dropna(how="all")

def calculate_returns(price_df):
    return price_df.pct_change().dropna()
