import pprint

from pytdx.config.hosts import hq_hosts
from pytdx.hq import TdxHq_API
from pytdx.pool.hqpool import TdxHqPool_API
from pytdx.pool.ippool import AvailableIPPool

from THS.THSTrader import THSTrader, THSWithdrawWatcher
from main import env


class App:
    def __init__(self):
        self.trader = THSTrader(env.serialno)

    def fresh_ips(self):
        ips = [(v[1], v[2]) for v in hq_hosts]

        ## IP 池对象
        ippool = AvailableIPPool(TdxHq_API, ips)

        ## 选出M, H
        primary_ip, hot_backup_ip = ippool.sync_get_top_n(2)

        print("make pool api")
        ## 生成hqpool对象，第一个参数为TdxHq_API后者 TdxExHq_API里的一个，第二个参数为ip池对象。
        api = TdxHqPool_API(TdxHq_API, ippool)

        ## connect 函数的参数为M, H 两组 (ip, port) 元组
        with api.connect(primary_ip, hot_backup_ip):
            ## 这里的借口和对应TdxHq_API 或者 TdxExHq_API里的一样，我们通过反射调用正确的接口
            ret = api.get_xdxr_info(0, '000001')
            print("send api call done")
            pprint.pprint(ret)

    def listen_withdrawals(self):
        pass

    def __insert_stocks(self,stocks):
        print(stocks)
        pass

    def __delete_stocks(self,stocks):
        print(stocks)
        pass

    def run(self):
        watcher = THSWithdrawWatcher(self.trader,self.__insert_stocks,self.__delete_stocks)
        watcher.start()

