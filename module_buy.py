import yfinance as yf
import numpy as np

def Buy(asset, portfolio_item, ratio, start_date, end_date, commission=0.002):
    portfolio_dict = {}
    buying_price = {}
    buying_vol = {}
    transaction = {}

    remain = []

    #     start_date = "2022-01-01"
    #     end_date = "2023-11-02"
    for i in range(len(portfolio_item)):
        ticker = yf.Ticker(portfolio_item[i])
        portfolio_dict[portfolio_item[i]] = ticker.history(start=start_date, end=end_date)
        buying_price[portfolio_item[i]] = np.mean(np.array(portfolio_dict[portfolio_item[i]])[0, 1:3])

        tmp = np.floor(asset * ratio[i] / buying_price[portfolio_item[i]])
        if len(portfolio_item) > 1:
            if tmp * buying_price[portfolio_item[i]] + commission * tmp * buying_price[portfolio_item[i]] < asset * \
                    ratio[i]:
                buying_vol[portfolio_item[i]] = np.floor(asset * ratio[i] / buying_price[portfolio_item[i]])[0]
            else:
                buying_vol[portfolio_item[i]] = np.floor(asset * ratio[i] / buying_price[portfolio_item[i]])[0] - 1
        else:
            if tmp * buying_price[portfolio_item[i]] + commission * tmp * buying_price[portfolio_item[i]] < asset * \
                    ratio[i]:
                buying_vol[portfolio_item[i]] = np.floor(asset * ratio[i] / buying_price[portfolio_item[i]])
            else:
                buying_vol[portfolio_item[i]] = np.floor(asset * ratio[i] / buying_price[portfolio_item[i]]) - 1

        transaction[portfolio_item[i]] = commission * buying_price[portfolio_item[i]] * buying_vol[portfolio_item[i]]

    remain = asset - np.sum(np.array(list(buying_price.values())) * np.array(list(buying_vol.values()))) - np.sum(
        np.array(list(transaction.values())))
    #     print(portfolio_dict.items())
    portfolio_wallet = sum(portfolio_dict.values())
    return portfolio_wallet, portfolio_dict, buying_price, buying_vol, transaction, remain
