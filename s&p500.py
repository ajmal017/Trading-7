from datetime import datetime
from ib_insync import *
import asyncio
import json
import math
import redis
import pandas as pd 
import numpy as np
import time

r = redis.Redis(host="10.0.0.213", port=6379, charset="utf-8", decode_responses=True,db=3)
util.startLoop()
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12)
pd.options.display.max_rows = 252
pd.set_option('precision', 2)

## Get S&P500 list

payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
pd.DataFrame(payload[0]).to_csv("S&P500.csv")
pd.read_csv("S&P500.csv")

r.flushall()

start_time = datetime.now()
no_of_API_requests = 50

async def main():       
    with await IB().connectAsync(port=7497) as ib:   
        stocklist=np.array_split(pd.read_csv("S&P500.csv").Symbol.tolist(), no_of_API_requests)
        for eachstocklist in stocklist:
            if len(eachstocklist) <= 45:                
                contracts = [Stock(symbol=eachstock, exchange='SMART', currency='USD')
                            for eachstock in eachstocklist]                 
                tasks = [ib.reqHistoricalDataAsync(s, endDateTime='',
                                                durationStr='1 D',
                                                barSizeSetting='1 day',
                                                whatToShow='TRADES',
                                                useRTH=True,
                                                formatDate=1) for s in contracts]
                
                result =  await asyncio.gather(*tasks)
                for i in result:  
                    if i:                        
                        print("Writing Data for:",i.contract.symbol)                        
                        df = util.df(i)
                        if not df.empty:
                            df['date']=df.date.astype(str)
                            r.set(i.contract.symbol,df.to_json())
asyncio.run(main())
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

data = r.get('AAPL')
pd.DataFrame(json.loads(data))
pd.DataFrame(json.loads(data)).close[-1]

