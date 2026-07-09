import numpy as np


def annualized_return(returns):
    return returns.mean() * 252


def annualized_volatility(returns):
    return returns.std() * np.sqrt(252)


def sharpe_ratio(returns, risk_free_rate=0.03):
    ann_ret = annualized_return(returns)
    ann_vol = annualized_volatility(returns)
    return (ann_ret - risk_free_rate) / ann_vol


def max_drawdown(cumulative_returns):
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    return drawdown.min()


def value_at_risk(returns, confidence=0.95):
    return np.percentile(returns, (1 - confidence) * 100)
