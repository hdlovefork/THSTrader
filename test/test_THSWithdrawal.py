import unittest

from test import env, measure_time
from THS.THSAction import THSAction
from THS.THSWithdrawal import THSWithdrawal


class TestTHSWithdrawal(unittest.TestCase):
    def setUp(self) -> None:
        self.action = THSAction(env.serialno)
        self.withdrawal = THSWithdrawal(self.action, env)

    def test_execute_when_tick_bid_vol1_less_than_env_bid_vol1(self):
        stocks = [
            {'market': 0, 'name': '金发拉比', 'code': '002762', 'bid_vol1': 100},
            {'market': 0, 'name': '尚荣医疗', 'code': '002551', 'bid_vol1': 100}
        ]
        withdraw_stocks = self.action.get_avail_withdrawals_ex(False)
        for s in withdraw_stocks:
            s['bid_vol1'] = 100
            stocks.append(s)
        self.withdrawal.env.withdrawal.top.bid_vol1 = 200
        if len(withdraw_stocks):
            r = measure_time(self.withdrawal.resolve, stocks)
            self.assertNotEqual(None, r)

    def test_execute_when_tick_bid_vol1_less_than_env_bid_vol1_rate(self):
        stocks = [
            {'market': 0, 'name': '金发拉比', 'code': '002762', 'bid_vol1': 70},
            {'market': 0, 'name': '尚荣医疗', 'code': '002551', 'bid_vol1': 100}
        ]
        stock = stocks[0].copy()
        stock['bid_vol1'] = 100
        self.withdrawal.last_tick[stocks[0]['code']] = stock
        r = measure_time(self.withdrawal.resolve, stocks)

        self.assertNotEqual(None, r)
