#!/usr/bin/env python3

import numpy as np
import yfinance as yf
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

start_epoch = '2019-11-14'
end_epoch = '2022-11-14'

stocks = defaultdict(lambda: defaultdict(dict))
stocks['benchmark']['S&P 500']['ticker'] = '^GSPC'
#stocks['benchmark']['Dow Jones']['ticker'] = '^DJI'
#stocks['benchmark']['Nasdaq']['ticker'] = '^IXIC'

# NFL
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
stocks['NFL']['Tennessee Titans: Nissan']['ticker'] = 'NSANY'
stocks['NFL']['Houston Texans: NRG Energy']['ticker'] = 'NRG'
stocks['NFL']['Cincinnati Bengals: Paycor HCM']['ticker'] = 'PYCR'
stocks['NFL']['Tampa Bay Buccaneers: Raymond James Financial']['ticker'] = 'RJF'
stocks['NFL']['LA Rams/Chargers: SoFi Technologies Inc']['ticker'] = 'SOFI'
stocks['NFL']['Minnesota Vikings: US Bancorp']['ticker'] = 'USB'

stocks['NBA']['Dallas Mavericks: American Airlines']['ticker'] = 'AAL'
stocks['NBA']['San Antonio Spurs: AT&T']['ticker'] = 'T'
stocks['NBA']['Denver Nuggets: Ball Corporation']['ticker'] = 'BALL'
stocks['NBA']['Brooklyn Nets: Barklays PLC']['ticker'] = 'BCS'
stocks['NBA']['Washington Wizards: Capitol One']['ticker'] = 'COF'
stocks['NBA']['Golden State Warriors: JPMorgan Chase & Co']['ticker'] = 'JPM'
stocks['NBA']['LA Clippers/Lakers: Crypto dot com']['ticker'] = 'CRCW'
stocks['NBA']['Memphis Grizzlies: FedEx']['ticker'] = 'FDX'
stocks['NBA']['Milwaukee Bucks: Fiserv Inc']['ticker'] = 'FISV'
stocks['NBA']['Miami Heat: FTX']['ticker'] = -100
stocks['NBA']['Oklahoma City Thunder: Paycom Software Inc']['ticker'] ='PAYC'
stocks['NBA']['Cleveland Cavaliers: Rocket Mortgage']['ticker'] ='RKT'
stocks['NBA']['Toronto Raptors: Scotiabank']['ticker'] ='BNS'
stocks['NBA']['Charlotte Hornets: Spectrum Brands Holdings Inc']['ticker'] ='SPB'
stocks['NBA']['Minnesota Timberwolves: Target']['ticker'] ='TGT'
stocks['NBA']['Boston Celtics: TD Bank']['ticker'] ='TD'
stocks['NBA']['Houston Rockets: Toyota']['ticker'] ='TM'
stocks['NBA']['Chicago Bulls: United Airlines']['ticker'] ='UAL'
stocks['NBA']['Utah Jazz: Vivint']['ticker'] ='VVNT'
stocks['NBA']['Philadelphia 76ers: Wells Fargo']['ticker'] ='WFC'

#stocks['MLB']['Tampa Bay Buccaneers: Raymond James Financial']['ticker'] = 'RJF'
#stocks['MLB']['LA Rams/Chargers: SoFi Technologies Inc']['ticker'] = 'SOFI'
#stocks['MLB']['Minnesota Vikings: US Bancorp']['ticker'] = 'USB'


# collect data
for league in stocks:
    for stadium in stocks[league]:
        ticker = stocks[league][stadium]['ticker']
        if type(ticker) == str:
            data = yf.download([ticker], start=start_epoch, end=end_epoch, group_by='ticker')
            start_price = data.iloc[0]['Open']
            end_price = data.iloc[-1]['Open']
            pct_change = (end_price-start_price)/start_price*100
        else:
            pct_change = ticker
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
            row_dict['league'] = league

        row = pd.DataFrame(row_dict,index=[stadium])
        condensed_df = pd.concat([condensed_df,row],axis=0)

condensed_df.sort_values(by='rel to S&P 500', inplace=True)

print(condensed_df)



fig, ax = plt.subplots()
n = condensed_df.shape[0]
colors = {'NFL':'red', 'NBA': 'blue'}
c = condensed_df['league'].apply(lambda x: colors[x])
ax.barh(range(n), condensed_df['rel to S&P 500'], color=c)

# hacky crap to make legend work
for i, j in colors.items(): #Loop over color dictionary
    ax.barh(range(n), condensed_df['rel to S&P 500'],height=0,color=j,label=i) #Plot invisible bar graph but have the legends specified

ax.set_yticks(range(n), labels=condensed_df.index.values.tolist())
ax.invert_yaxis()
ax.set_title('3-Year Performance Relative to S&P 500')
ax.legend()



plt.tight_layout()
plt.show()



