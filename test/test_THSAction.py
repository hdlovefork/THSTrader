import time
import unittest

from THS.THSAction import THSAction
from test import env, measure_time


class TestTHSAction(unittest.TestCase):
    def setUp(self) -> None:
        self.action = THSAction(env.serialno)

    def test_withdrawals(self):
        withdrawals = measure_time(self.action.get_avail_withdrawals_ex)
        for v in withdrawals:
            print(v)

    def test_enter_withdrawals(self):
        self.action.enter_withdrawals_page()

    def test_click_refresh(self):
        self.action.click('刷新')

    def test_withdraw_chedan(self):
        withdraw_stocks = self.action.get_avail_withdrawals_ex(False)
        if len(withdraw_stocks) > 0:
            stock = withdraw_stocks[0]
            self.assertNotEqual(None, self.action.withdraw_dialog_chedan_when(0, lambda s: s['stock_name'] == stock['stock_name']))