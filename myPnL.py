from ib_insync import *
import asyncio
import os
import redis

r = redis.Redis(host="10.0.0.213", port=6379, charset="utf-8", decode_responses=True,db=3)
r.set('Name', 'SomeName')
data = r.get('Name')





def IntraDayPnL(ProfitLoss):
    a = "Profit:" if ProfitLoss.unrealizedPnL >= 0 else "Loss:"
    print(a+":"+str(ProfitLoss.unrealizedPnL))

def ExecutedOrders(trade,fill):
    print("\nIn ExecutedOrders Function\n")
    print(trade,fill)

def ExecutionErrors(reqId, errorCode, errorString, contract):
    print("In Error")
    print(reqId, errorCode, errorString, contract)

def ConnectedTWS():
    print("In Connected\n")    
    print([v for v in ib.accountValues() if v.tag == 'NetLiquidationByCurrency' and v.currency == 'BASE'])
    
def CurrentPositions(position):
    print("\n\nIn Position\n")
    print(position)

def CommissionReport(trade, fill, report):
    print("\n In CommissionReport\n")
    print(report.commission)

def onBarUpdate(bars, hasNewBar):
    # print(bars[-1])
    pass

def DisconnectedTWS():
    IB.sleep(0)
    print("Disconnected TWS")

async def hello():
    print("Starting Asyncio Program:")    
    await asyncio.sleep(0)    
    ib.reqPnL('DU1449161')                  ## Subscribe to PnL so pnlEvent can keep the PnL State current
    print(await ib.reqHistoricalDataAsync(contract, endDateTime='',
                                           durationStr='1 D',
                                           barSizeSetting='1 hour',
                                           whatToShow='TRADES',
                                           useRTH=False,
                                           formatDate=1))
    print("\n\nreqMktData\n\n",ib.reqMktData(contract))

ib = IB()
ib.connectedEvent += ConnectedTWS
ib.connect('127.0.0.1', 7497, clientId=0)
contract = Stock('TSLA', 'SMART', 'USD')
# ticker = ib.ticker(contract)
# ib.sleep(2)
# print("Ticker Price: ",ticker)
ib.pnlEvent += IntraDayPnL
ib.execDetailsEvent += ExecutedOrders
ib.errorEvent += ExecutionErrors
ib.positionEvent += CurrentPositions
ib.commissionReportEvent += CommissionReport
bars = ib.reqRealTimeBars(contract, 5, 'TRADES', False)
bars.updateEvent += onBarUpdate
ib.disconnectedEvent += DisconnectedTWS

#  IB.run()   

##################################################################################################
## Below block with Asyncio
try:
    loop = asyncio.get_event_loop()
    loop.create_task(hello())    
    loop.run_forever()
except KeyboardInterrupt:
    ib.disconnect()
    os.system('clear')    
    print("User Closed the connection")
##################################################################################################

## Notes    
# If you just want to ping TWS to see if it's still there then you could use ib.reqCurrentTime() - this request is served locally from TWS with no traffic to the IB server.

# https://github.com/erdewit/ib_insync/pull/276/files/2f12010d77fef3b883642a22d3761b8567c6e0fe
