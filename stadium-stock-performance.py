#!/usr/bin/env python3

import numpy as np
import yfinance as yf
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

start_epoch = '2019-11-13'
end_epoch = '2022-11-13'

stocks = defaultdict(lambda: defaultdict(dict))
stocks['benchmark']['S&P 500']['ticker'] = '^GSPC'
stocks['benchmark']['Dow Jones']['ticker'] = '^DJI'
stocks['benchmark']['Nasdaq']['ticker'] = '^IXIC'

stocks['NFL']['Las Vegas Raiders: Allegiant Travel Company']['ticker'] = 'ALGT'
stocks['NFL']['Dallas Cowboys: AT&T']['ticker'] = 'T'
stocks['NFL']['New Orleans Saints: Caesars']['ticker'] = 'CZR'
stocks['NFL']['Washington Commanders: FedEx']['ticker'] = 'FDX'
stocks['NFL']['Cleveland Browns: FirstEnergy']['ticker'] = 'FE'
stocks['NFL']['New England Patriots: Proctor and Gamble']['ticker'] = 'PG'
stocks['NFL']['San Francisco 49ers: Levis']['ticker'] = 'LEVI'
stocks['NFL']['Philadelphia Eagles: Lincoln National Corp']['ticker'] = 'LNC'
stocks['NFL']['Seattle Seahawks: Lumen Technologies']['ticker'] = 'LUMN'
stocks['NFL']['Baltimore Ravens: M&T Bank']['ticker'] = 'MTB'
stocks['NFL']['Atlanta Falcons: Mercedes Benz']['ticker'] = 'MBGYY'
stocks['NFL']['New York Jets/Giants: Metlife']['ticker'] = 'MET'


# collect data
for league in stocks:
    for stadium in stocks[league]:
        ticker = stocks[league][stadium]['ticker']
        data = yf.download([ticker], start=start_epoch, end=end_epoch, group_by='ticker')
        start_price = data.iloc[0]['Open']
        end_price = data.iloc[-1]['Open']
        pct_change = (end_price-start_price)/start_price*100
        stocks[league][stadium]['percentage change'] = pct_change

# condense data
condensed_df = pd.DataFrame()

for league in stocks:
    if league == 'benchmark':
        continue
    for stadium in stocks[league]:
        row_dict = defaultdict(lambda: defaultdict(dict))
        stock_perf = stocks[league][stadium]['percentage change']
        for benchmark in stocks['benchmark']:
            benchmark_perf = stocks['benchmark'][benchmark]['percentage change']

            row_dict['rel to ' + benchmark] = stock_perf-benchmark_perf

        row = pd.DataFrame(row_dict,index=[stadium])
        condensed_df = pd.concat([condensed_df,row],axis=0)

print(condensed_df)

