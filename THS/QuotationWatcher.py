import threading

from log import log


class QuotationWatcher:
    def __init__(self, quotation, quote_callback=None):
        self.wait_interval = 0.5
        self.worker_thread = None
        self.thread_lock = threading.Lock()
        self.stop_event = threading.Event()
        self.watch_stocks = []
        self.quotation = quotation
        self.quote_callback = quote_callback

    def append_watch_stock(self, stock):
        # 判断stock是否为list或者tuple类型，如果是则遍历添加，否则直接添加
        if isinstance(stock, (list, tuple)):
            for s in stock:
                self.watch_stocks.append(s)
        else:
            self.watch_stocks.append(stock)

    def remove_watch_stock(self, stock):
        # 判断stock是否为list或者tuple类型，如果是则遍历删除，否则直接删除
        if isinstance(stock, (list, tuple)):
            for s in stock:
                self.watch_stocks.remove(s)
        else:
            self.watch_stocks.remove(stock)

    def __worker(self):
        log.info("正在监控股票行情...")
        while not self.stop_event.is_set():
            with self.thread_lock:
                if self.quote_callback is not None and len(self.watch_stocks) > 0:
                    stocks = [(s['market_code'], s['stock_code']) for s in self.watch_stocks]
                    log.debug("正在获取股票行情: %s" % stocks)
                    quot_stocks = self.quotation.get_security_quotes(stocks)
                    # 在返回的行情数据里面添加股票名称name
                    for qs in quot_stocks:
                        for ws in self.watch_stocks:
                            if ws['stock_code'] == qs['code']:
                                qs['name'] = ws['stock_name']
                                break
                    self.quote_callback(quot_stocks)
            self.stop_event.wait(self.wait_interval)

    def start_watch(self):
        self.worker_thread = threading.Thread(target=self.__worker)
        self.worker_thread.start()

    def stop_watch(self):
        self.stop_event.set()
        if self.worker_thread.is_alive():
            self.worker_thread.join()
        self.worker_thread = None
