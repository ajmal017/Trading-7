from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)      
    
    def error(self, reqId, errorCode, errorString):        
        print("Error. Id:", reqId, "Code:", errorCode, "Msg:", errorString)

    def historicalData(self, reqId, bar):
        print("DATE:", bar.date, "Open:", bar.open, "High:", bar.high)


def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, clientId=1)
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"

    app.reqHistoricalData(1, contract, "", "1 D", "1 min", "MIDPOINT", 0, 1, False, [])
    app.run()


if __name__ == "__main__":
    main()    
