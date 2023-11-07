import numpy as np

def SellAll(portfolio, portfolio_item, vol, remain, commission = 0.002):
    selling_price = np.mean(np.array(portfolio[portfolio_item])[-1, [0, 3]])
    remain = selling_price * vol[portfolio_item] + remain - commission * selling_price * vol[portfolio_item]
    return remain, selling_price