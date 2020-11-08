from ib_insync import *
import pandas as pd 
import numpy as np
import time
util.startLoop()
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=10)
pd.options.display.max_rows = 252
pd.set_option('precision', 2)


stockhdata = await ib.reqHistoricalDataAsync(Stock('SPY', 'SMART', 'USD'), endDateTime='',
                                        durationStr='1 Y',
                                        barSizeSetting='1 day',
                                        whatToShow='TRADES',
                                        useRTH=True,
                                        formatDate=1)

df = pd.DataFrame(stockhdata)                                        

df['Change'] = df['close'].pct_change(periods=1)*100
df['Change']=df['Change'].round(2)
df['Gap']= np.where(df['Change'] >= 2,"GapUp",np.where(df['Change'] <= -2,"GapDown",""))
df['52WeekHigh'] = max(df.high)
df['52WeekLow'] = min(df.low)
df['SMA_9'] = df.close.rolling(window=9).mean()
df['SMA_20'] = df.close.rolling(window=20).mean()
df['SMA_50'] = df.close.rolling(window=50).mean()
df['SMA_100'] = df.close.rolling(window=100).mean()
df['SMA_200'] = df.close.rolling(window=200).mean()
df['Volume_20'] = df.volume.rolling(window=20).mean()
df['How-Far-From-is-closing-from-52Week-High'] = df.apply(lambda x: fxy(x['52WeekHigh'], x['close']), axis=1)
df['How-Far-From-is-closing-from-52Week-Low'] = df.apply(lambda x: fxy(x['52WeekLow'], x['close']), axis=1)
df['How-Far-From-is-closing-from-SMA_200'] = df.apply(lambda x: fxy(x['SMA_200'], x['close']), axis=1)
df['How-Far-From-is-closing-from-SMA_100'] = df.apply(lambda x: fxy(x['SMA_100'], x['close']), axis=1)
df['How-Far-From-is-closing-from-SMA_50'] = df.apply(lambda x: fxy(x['SMA_50'], x['close']), axis=1)
df['How-Far-From-is-closing-from-SMA_20'] = df.apply(lambda x: fxy(x['SMA_20'], x['close']), axis=1)
