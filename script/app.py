from THS.QuotationWatcher import QuotationWatcher
from THS.THSQuotation import THSQuotation
from THS.THSTrader import THSAction, THSWithdrawWatcher

from THS.THSWithdrawal import THSWithdrawal
from log import log


class App:
    def __init__(self, env):
        self.env = env
        self.trader = THSAction(env.serialno)
        self.quotation = THSQuotation(env.ipspath)
        self.quotation_watcher = QuotationWatcher(self.quotation, self.__listen_quotation)
        self.watcher = THSWithdrawWatcher(self.trader, self.__insert_stocks, self.__delete_stocks)
        self.withdrawals = THSWithdrawal(self.trader,env)

    def __listen_quotation(self, quot_stocks):
        self.withdrawals.resolve(quot_stocks)

    def __insert_stocks(self, stocks):
        self.quotation_watcher.append_watch_stock(stocks)

    def __delete_stocks(self, stocks):
        self.quotation_watcher.remove_watch_stock(stocks)

    def run(self):
        try:
            self.watcher.start()
            self.quotation_watcher.start_watch()

            # 提示用户输入exit退出程序
            while True:
                cmd = input("请输入命令(exit退出)：")
                if cmd == "exit":
                    break
        except Exception as e:
            log.exception(e)
        finally:
            log.info("正在退出程序...")
            self.quotation_watcher.stop_watch()
            self.watcher.stop()
            self.quotation.close()
