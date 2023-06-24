import time
import unittest

from THS.THSTrader import THSTrader, THSWithdrawWatcher
from main import env


class TestTHSTrader(unittest.TestCase):
    def setUp(self) -> None:
        self.trader = THSTrader(env.serialno)

    def test_withdrawals(self):
        withdrawals = self.measure_time(self.trader.get_avail_withdrawals_ex, False)
        for withdrawal in withdrawals:
            print(withdrawal)

    def test_enter_withdrawals(self):
        self.trader.enter_withdrawals_page()

    def measure_time(self, func, *args, **kwargs):
        start_time = time.time()
        r = func(*args, **kwargs)
        end_time = time.time()
        print("执行时间为：{} 秒".format(end_time - start_time))
        return r

    def test_click_refresh(self):
        self.trader.click('//*[@resource-id="com.hexin.plat.android:id/title_bar_right_container"]//*[@resource-id="com.hexin.plat.android:id/title_bar_img"]')