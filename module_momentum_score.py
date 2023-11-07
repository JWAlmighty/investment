from datetime import timedelta
import numpy as np
def momentum_score(item, calc_date):
    back_date = {}
    scores = {}
    # 1 month score
    date_1 = calc_date - timedelta(days=30)
    while True:
        try:
            #             print(date_1)
            momentum1 = item[date_1.isoformat():calc_date.isoformat()]
            break
        except:
            date_1 = date_1 - timedelta(days=1)
    back_date['month1'] = date_1
    scores['month1'] = (momentum1['Close'][-1] - momentum1['Close'][0]) / momentum1['Close'][0]

    # 3 months score
    date_3 = calc_date - timedelta(days=92)
    while True:
        try:
            #             print(date_2)
            momentum3 = item[date_3.isoformat():calc_date.isoformat()]
            break
        except:
            date_3 = date_3 - timedelta(days=1)
    back_date['month3'] = date_3
    scores['month3'] = (momentum3['Close'][-1] - momentum3['Close'][0]) / momentum3['Close'][0]

    # 6 months score
    date_6 = calc_date - timedelta(days=183)
    while True:
        try:
            #             print(date_6)
            momentum6 = item[date_6.isoformat():calc_date.isoformat()]
            break
        except:
            date_6 = date_6 - timedelta(days=1)
    back_date['month6'] = date_6
    scores['month6'] = (momentum6['Close'][-1] - momentum6['Close'][0]) / momentum6['Close'][0]

    # 12 months score
    date_12 = calc_date - timedelta(days=365)
    while True:
        try:
            #             print(date_12)
            momentum12 = item[date_12.isoformat():calc_date.isoformat()]
            break
        except:
            date_12 = date_12 - timedelta(days=1)
    back_date['month12'] = date_12
    scores['month12'] = (momentum12['Close'][-1] - momentum12['Close'][0]) / momentum12['Close'][0]

    final_score = np.sum(np.array([12, 4, 2, 1]) * np.array(list(scores.values())))
    return final_score, back_date, scores