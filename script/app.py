from THS.THSQuotation import THSQuotation
from THS.THSTrader import THSTrader, THSWithdrawWatcher
from main import env


class App:
    def __init__(self):
        self.trader = THSTrader(env.serialno)
        self.quotation = THSQuotation(env.ipspath)

    def listen_withdrawals(self):
        pass

    def __insert_stocks(self,stocks):
        print(f'添加：{stocks}')
        pass

    def __delete_stocks(self,stocks):
        print(f'删除：{stocks}')
        pass

    def run(self):
        watcher = THSWithdrawWatcher(self.trader,self.__insert_stocks,self.__delete_stocks)
        watcher.start()

