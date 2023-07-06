import unittest

from THS.THSAction import THSAction, calc_md5
from test import env, measure_time


class TestTHSAction(unittest.TestCase):
    def setUp(self) -> None:
        self.action = THSAction(env.serial_no)

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

    def test_withdrawals_page_hierarchy(self):
        content = measure_time(self.action.withdrawals_page_hierarchy)
        self.assertIsNotNone(content)

    def test_calc_md5(self):
        content = self.action.withdrawals_page_hierarchy()
        md5 = measure_time(calc_md5, content)
        self.assertIsNotNone(md5)

    def test_get_withdrawals_page_hierarchy_and_calc_md5(self):
        md5 = measure_time(self.get_withdrawals_page_hierarchy_and_calc_md5)
        self.assertIsNotNone(md5)

    def get_withdrawals_page_hierarchy_and_calc_md5(self):
        content = self.action.withdrawals_page_hierarchy()
        return calc_md5(content)