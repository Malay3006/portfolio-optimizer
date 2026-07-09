import numpy as np
from scipy.optimize import minimize


def portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate=0.03):
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    sharpe = (returns - risk_free_rate) / std
    return returns, std, sharpe


def negative_sharpe(weights, mean_returns, cov_matrix, risk_free_rate):
    return -portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate)[2]


def portfolio_volatility(weights, mean_returns, cov_matrix):
    return portfolio_performance(weights, mean_returns, cov_matrix)[1]


def max_sharpe_portfolio(mean_returns, cov_matrix, risk_free_rate=0.03):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    init_guess = num_assets * [1. / num_assets]
    result = minimize(negative_sharpe, init_guess, args=args,
                       method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x


def min_volatility_portfolio(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    init_guess = num_assets * [1. / num_assets]
    result = minimize(portfolio_volatility, init_guess, args=args,
                       method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x


def efficient_frontier(mean_returns, cov_matrix, returns_range):
    efficient_portfolios = []
    num_assets = len(mean_returns)
    for target in returns_range:
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: portfolio_performance(x, mean_returns, cov_matrix)[0] - target}
        )
        bounds = tuple((0, 1) for _ in range(num_assets))
        init_guess = num_assets * [1. / num_assets]
        result = minimize(portfolio_volatility, init_guess, args=(mean_returns, cov_matrix),
                           method='SLSQP', bounds=bounds, constraints=constraints)
        if result.success:
            efficient_portfolios.append(result.x)
    return efficient_portfolios
