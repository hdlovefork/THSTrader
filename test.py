# -*- coding: utf-8 -*-

from THS.THSTrader import THSTrader
import time

import ssl

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context

    trader = THSTrader(r"127.0.0.1:62001")    # 连接客户端

    # print(trader.get_balance())                            # 获取当前可用资金

    # print(trader.get_position())                           # 获取当前持有的股票

    print(trader.get_avail_withdrawals())                  # 获取可撤单的股票

    # print(trader.sell(stock_no="162411", amount=100, price=0.238))  # 卖出股票
    #
    # result = trader.buy(stock_no="162411", amount=100, price=0.218)  # 买入股票
    # print(result)
    # time.sleep(5)
    # if result["success"] == True:						   # 如果买入下单成功，尝试撤单
    #     print("撤单测试--->", end="")
    #     print(trader.withdraw(entrust_no=result["entrust_no"]))

