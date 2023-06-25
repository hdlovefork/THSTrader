import time
import unittest

from THS.THSTrader import THSTrader, THSWithdrawWatcher
from test import env, measure_time


class TestTHSTrader(unittest.TestCase):
    def setUp(self) -> None:
        self.trader = THSTrader(env.serialno)

    def test_withdrawals(self):
        withdrawals = measure_time(self.trader.get_avail_withdrawals_ex)
        print(withdrawals)

    def test_enter_withdrawals(self):
        self.trader.enter_withdrawals_page()

    def test_click_refresh(self):
        self.trader.click('//*[@resource-id="com.hexin.plat.android:id/title_bar_right_container"]//*[@resource-id="com.hexin.plat.android:id/title_bar_img"]')

    def test_ips(self):
        pass