# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from module_buy import Buy
from module_sellAll import SellAll
from module_momentum_score import momentum_score
import numpy as np
from datetime import timedelta
import yfinance as yf
import pandas as pd
import quantstats as qs
from matplotlib import pyplot as plt



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 공격형
    prev_item = 'default'
    start_date = "2004-01-01"
    end_date = "2023-11-05"
    # start_date = "2011-04-24"
    # end_date = "2011-07-30"
    ticker = yf.Ticker("SPY")  # 미국 주식
    spy = ticker.history(start=start_date, end=end_date)

    ticker = yf.Ticker("EFA")  # 선진국 주식
    efa = ticker.history(start=start_date, end=end_date)

    ticker = yf.Ticker("EEM")  # 개발도상국 주식
    eem = ticker.history(start=start_date, end=end_date)

    ticker = yf.Ticker("AGG")  # 미국 혼합채권 주식
    agg = ticker.history(start=start_date, end=end_date)

    # 안전자산
    ticker = yf.Ticker("LQD")  # 미국 회사채
    lqd = ticker.history(start=start_date, end=end_date)

    ticker = yf.Ticker("IEF")  # 미국 중기 국채
    ief = ticker.history(start=start_date, end=end_date)

    ticker = yf.Ticker("SHY")  # 미국 단기 국채
    shy = ticker.history(start=start_date, end=end_date)
    # print("Done")
    rebalance_day = shy.index[0] + timedelta(days=30)
    backtesting = {}
    remain = 10000
    item_aggressive = ['spy', 'efa', 'eem', 'agg']
    item_safe = ['lqd', 'ief', 'shy']
    # portfolio_wallet, portfolio_dict, buying_price, buying_vol, transaction, remain = Buy(asset = 10000, portfolio_item = ['SPY'], ratio = [1], start_date = "2022-01-01", end_date = "2022-11-02")
    # SellAll(portfolio_dict, 'SPY', buying_vol, remain)

    while rebalance_day < shy.index[-1]:

        score_spy, _, _ = momentum_score(spy, rebalance_day)
        score_efa, _, _ = momentum_score(efa, rebalance_day)
        score_eem, _, _ = momentum_score(eem, rebalance_day)
        score_agg, _, _ = momentum_score(agg, rebalance_day)

        score_lqd, _, _ = momentum_score(lqd, rebalance_day)
        score_ief, _, _ = momentum_score(ief, rebalance_day)
        score_shy, _, _ = momentum_score(shy, rebalance_day)

        scores_tmp = [score_spy, score_efa, score_eem, score_agg, score_lqd, score_ief, score_shy]
        for score in scores_tmp[:4]:
            if score < 0:
                strategy = -1
                break
            else:
                strategy = 1
        if strategy == 1:
            item = item_aggressive[np.argmax(scores_tmp[:4])]
            # print(item)
            if item == prev_item:
                _, portfolio_dict, _, buying_vol, _, remain = Buy(asset=remain, portfolio_item=[item], ratio=[1],
                                                                  start_date=rebalance_day.isoformat()[:10],
                                                                  end_date=(rebalance_day + timedelta(days=30)).isoformat()[
                                                                           :10], commission=0)
                remain, sell_price = SellAll(portfolio_dict, item, buying_vol, remain, commission=0)
            else:
                _, portfolio_dict, _, buying_vol, _, remain = Buy(asset=remain, portfolio_item=[item], ratio=[1],
                                                                  start_date=rebalance_day.isoformat()[:10],
                                                                  end_date=(rebalance_day + timedelta(days=30)).isoformat()[
                                                                           :10], commission=0.002)
                remain, sell_price = SellAll(portfolio_dict, item, buying_vol, remain)
            prev_item = item
        else:
            item = item_safe[np.argmax(scores_tmp[4:])]
            if item == prev_item:
                _, portfolio_dict, _, buying_vol, _, remain = Buy(asset=remain, portfolio_item=[item], ratio=[1],
                                                                  start_date=rebalance_day.isoformat()[:10],
                                                                  end_date=(rebalance_day + timedelta(days=30)).isoformat()[
                                                                           :10], commission=0)
                remain, sell_price = SellAll(portfolio_dict, item, buying_vol, remain, commission=0)
            else:
                _, portfolio_dict, _, buying_vol, _, remain = Buy(asset=remain, portfolio_item=[item], ratio=[1],
                                                                  start_date=rebalance_day.isoformat()[:10],
                                                                  end_date=(rebalance_day + timedelta(days=30)).isoformat()[
                                                                           :10], commission=0.002)
                remain, sell_price = SellAll(portfolio_dict, item, buying_vol, remain)
            prev_item = item

        volume = buying_vol
        scores_tmp.append(strategy)
        scores_tmp.append(remain)
        scores_tmp.append(sell_price)
        scores_tmp.append(volume)
        backtesting[rebalance_day] = scores_tmp
        rebalance_day = rebalance_day + timedelta(days=30)

    pd.set_option('display.max_colwidth', None, 'display.max_rows', None)

    tmp = pd.DataFrame.from_dict(backtesting, orient='index',
                                 columns=['SPY', 'EFA', 'EEM', 'AGG', 'LQD', 'IEF', 'SHY', 'Strategy', 'Remain',
                                          'Price', 'Volume'])

    tmp.to_csv('tmp.csv')
    qs.reports.basic(tmp['Remain'])
    plt.plot(tmp.index, tmp['Remain'])
    # plt.plot(tmp.index, ief['Close'])
    plt.title("Remain")
    plt.show()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
