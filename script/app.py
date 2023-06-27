import time

from THS.QuotationWatcher import QuotationWatcher
from THS.TestThread import TestThread
from log import log
from THS.THSQuotation import THSQuotation
from THS.THSTrader import THSTrader, THSWithdrawWatcher
from script import env


class App:
    def __init__(self):
        self.trader = THSTrader(env.serialno)
        self.quotation = THSQuotation(env.ipspath)
        self.quotation_watcher = QuotationWatcher(self.quotation, self.listen_quotation)
        self.watcher = THSWithdrawWatcher(self.trader,self.__insert_stocks,self.__delete_stocks)

    def listen_quotation(self,quot_stocks):
        log.debug(quot_stocks)

    def __insert_stocks(self,stocks):
        self.quotation_watcher.append_watch_stock(stocks)

    def __delete_stocks(self,stocks):
        self.quotation_watcher.remove_watch_stock(stocks)

    def run(self):
        self.watcher.start()
        self.quotation_watcher.start_watch()

        # 提示用户输入exit退出程序
        while True:
            cmd = input("请输入命令(exit退出)：")
            if cmd == "exit":
                break
            time.sleep(1)
        log.info("正在退出程序...")
        self.quotation_watcher.stop_watch()
        self.watcher.stop()
        self.quotation.close()
