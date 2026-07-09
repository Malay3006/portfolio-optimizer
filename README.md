# Portfolio Optimizer

A Streamlit-based web application for building and analyzing optimized investment portfolios using Modern Portfolio Theory (MPT). The app fetches historical stock data, estimates expected returns and risk, and computes portfolio allocations that aim to maximize return per unit of risk.

## Overview

This project helps users:
- select a basket of tickers
- download historical price data
- calculate daily returns
- build optimized portfolios
- visualize the efficient frontier
- evaluate portfolio risk and performance

## Features

- Interactive Streamlit dashboard
- Portfolio optimization with:
  - Max Sharpe Ratio portfolio
  - Minimum Volatility portfolio
- Efficient Frontier visualization
- Risk and performance metrics:
  - Annualized Return
  - Annualized Volatility
  - Sharpe Ratio
  - Max Drawdown
  - 95% Value at Risk (VaR)
- Portfolio weight breakdown and growth chart

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- SciPy
- Plotly
- yfinance

## Project Structure

```text
portfolio-optimizer/
├── app.py                  # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── src/
    ├── data_loader.py     # Download and prepare market data
    ├── optimizer.py       # Portfolio optimization logic
    └── metrics.py         # Risk and performance metrics
```

## Installation

1. Clone the repository
   ```bash
   git clone <repo-url>
   cd portfolio-optimizer
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Run the App

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually http://localhost:8501).

## How the Model Works

The app follows a standard portfolio optimization workflow:

1. Data Collection
   - Historical adjusted close prices are downloaded using yfinance.

2. Return Calculation
   - Daily percentage returns are computed from price data.

3. Risk and Return Estimation
   - Mean daily returns are estimated.
   - A covariance matrix of returns is calculated.

4. Portfolio Optimization
   - The optimizer solves constrained optimization problems using SciPy's SLSQP method.
   - Weights are constrained to:
     - sum to 1
     - remain between 0 and 1

## Model Details

### 1. Max Sharpe Ratio Portfolio
This portfolio aims to maximize the Sharpe ratio:

$$
\text{Sharpe} = \frac{R_p - R_f}{\sigma_p}
$$

Where:
- $R_p$ = portfolio return
- $R_f$ = risk-free rate
- $\sigma_p$ = portfolio volatility

### 2. Minimum Volatility Portfolio
This portfolio minimizes portfolio volatility while keeping the portfolio fully invested.

### 3. Efficient Frontier
The app also constructs an efficient frontier by solving optimization problems for a range of target returns.

## Evaluation Metrics

The dashboard reports the following metrics for the optimized portfolios:

| Metric | Description |
|--------|-------------|
| Annualized Return | Expected yearly return based on historical returns |
| Annualized Volatility | Yearly risk measured as standard deviation |
| Sharpe Ratio | Risk-adjusted return measure |
| Max Drawdown | Largest peak-to-trough decline |
| 95% VaR | Estimated daily loss at 95% confidence |

## Example Usage

1. Enter tickers such as AAPL, MSFT, GOOGL, AMZN, TSLA
2. Choose the historical window length
3. Set the risk-free rate
4. Click "Run Optimization"
5. Review the portfolio allocation, frontier, and risk metrics

## Notes

- This project is intended for educational and research purposes.
- Historical data and optimization results are not guarantees of future performance.
- Portfolio optimization is sensitive to input data, estimation window, and assumptions.

## License

This project is open for educational and personal use.
