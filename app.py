import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date, timedelta

from src.data_loader import fetch_price_data, calculate_returns
from src.optimizer import (
    max_sharpe_portfolio, min_volatility_portfolio,
    portfolio_performance, efficient_frontier
)
from src.metrics import annualized_return, annualized_volatility, max_drawdown, value_at_risk

st.set_page_config(page_title="Portfolio Optimizer", layout="wide")

st.title("📈 Portfolio Management & Optimization System")
st.caption("Modern Portfolio Theory based portfolio construction and risk analysis")

with st.sidebar:
    st.header("Portfolio Settings")
    tickers_input = st.text_input("Tickers (comma-separated)", "AAPL,MSFT,GOOGL,AMZN,TSLA")
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    years_back = st.slider("Years of historical data", 1, 10, 5)
    risk_free_rate = st.number_input("Risk-free rate (annual)", value=0.03, step=0.01)
    run_button = st.button("Run Optimization", type="primary")

run_now = run_button or "results_loaded" not in st.session_state
if "results_loaded" not in st.session_state:
    st.session_state.results_loaded = True

if run_now:
    if len(tickers) < 2:
        st.error("Please enter at least 2 tickers.")
        st.stop()

    end_date = date.today()
    start_date = end_date - timedelta(days=365 * years_back)

    with st.spinner("Fetching market data..."):
        try:
            prices = fetch_price_data(tickers, start_date, end_date)
        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
            st.stop()

    if prices.empty:
        st.error("No data found for given tickers.")
        st.stop()

    returns = calculate_returns(prices)
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    max_sharpe_weights = max_sharpe_portfolio(mean_returns, cov_matrix, risk_free_rate)
    min_vol_weights = min_volatility_portfolio(mean_returns, cov_matrix)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Max Sharpe Ratio Portfolio")
        ret, vol, sharpe = portfolio_performance(max_sharpe_weights, mean_returns, cov_matrix, risk_free_rate)
        st.metric("Expected Annual Return", f"{ret*100:.2f}%")
        st.metric("Annual Volatility", f"{vol*100:.2f}%")
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")
        fig1 = go.Figure(data=[go.Pie(labels=tickers, values=max_sharpe_weights)])
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Minimum Volatility Portfolio")
        ret2, vol2, sharpe2 = portfolio_performance(min_vol_weights, mean_returns, cov_matrix, risk_free_rate)
        st.metric("Expected Annual Return", f"{ret2*100:.2f}%")
        st.metric("Annual Volatility", f"{vol2*100:.2f}%")
        st.metric("Sharpe Ratio", f"{sharpe2:.2f}")
        fig2 = go.Figure(data=[go.Pie(labels=tickers, values=min_vol_weights)])
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Efficient Frontier")
    target_returns = np.linspace(mean_returns.min() * 252, mean_returns.max() * 252, 50)
    frontier_weights = efficient_frontier(mean_returns, cov_matrix, target_returns / 252)
    frontier_points = [portfolio_performance(w, mean_returns, cov_matrix, risk_free_rate) for w in frontier_weights]

    if frontier_points:
        frontier_df = pd.DataFrame(frontier_points, columns=["Return", "Volatility", "Sharpe"])
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=frontier_df["Volatility"], y=frontier_df["Return"],
                                   mode="lines+markers", name="Efficient Frontier"))
        fig3.add_trace(go.Scatter(x=[vol], y=[ret], mode="markers",
                                   marker=dict(size=14, color="red"), name="Max Sharpe"))
        fig3.add_trace(go.Scatter(x=[vol2], y=[ret2], mode="markers",
                                   marker=dict(size=14, color="green"), name="Min Volatility"))
        fig3.update_layout(xaxis_title="Volatility (Risk)", yaxis_title="Expected Return")
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Risk Metrics (Max Sharpe Portfolio)")
    port_returns = (returns * max_sharpe_weights).sum(axis=1)
    cumulative = (1 + port_returns).cumprod()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Annualized Return", f"{annualized_return(port_returns)*100:.2f}%")
    m2.metric("Annualized Volatility", f"{annualized_volatility(port_returns)*100:.2f}%")
    m3.metric("Max Drawdown", f"{max_drawdown(cumulative)*100:.2f}%")
    m4.metric("95% VaR (daily)", f"{value_at_risk(port_returns)*100:.2f}%")

    st.subheader("Portfolio Growth (Backtest)")
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=cumulative.index, y=cumulative.values, mode="lines", name="Portfolio Value"))
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Optimal Weights (Max Sharpe)")
    weights_df = pd.DataFrame({"Ticker": tickers, "Weight": max_sharpe_weights})
    st.dataframe(weights_df.style.format({"Weight": "{:.2%}"}))

else:
    st.info("Set your tickers and click 'Run Optimization' to see results.")