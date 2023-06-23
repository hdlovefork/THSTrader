import time
import unittest

from THS.THSTrader import THSTrader
from test import env


class TestTHSTrader(unittest.TestCase):
    def setUp(self) -> None:
        self.trader = THSTrader(env.serialno)

    def test_withdrawals(self):
        start_time = time.time()
        withdrawals = self.trader.get_avail_withdrawals_ex()
        end_time = time.time()
        for withdrawal in withdrawals:
            print(withdrawal)
        print("执行时间为：{} 秒".format(end_time - start_time))
