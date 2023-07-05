import unittest

from test import env, measure_time
from THS.THSAction import THSAction
from THS.THSWithdrawal import THSWithdrawal


class TestTHSWithdrawal(unittest.TestCase):
    def setUp(self) -> None:
        self.action = THSAction(env.serial_no)
        self.withdrawal = THSWithdrawal(self.action, env)

    def test_resolve_when_tick_bid_vol1_less_than_env_bid_vol1(self):
        # 下个tick数据
        stocks = []
        withdraw_stocks = self.action.get_avail_withdrawals_ex()
        # 将当前买入委托单的买1手数设置为100作为下一次的tick数据
        for s in withdraw_stocks:
            s['code'] = s['stock_code']
            s['name'] = s['stock_name']
            s['bid_vol1'] = 100
            stocks.append(s.copy())

        # 配置文件设置为当买1手数小于200则撤单
        self.withdrawal.env.withdrawal.top.bid_vol1 = 200

        if len(withdraw_stocks) > 0:
            r = measure_time(self.withdrawal.resolve, stocks)
            self.assertEqual(len(stocks), len(r))

    def test_resolve_when_tick_bid_vol1_great_than_env_bid_vol1_rate(self):
        # 下个tick数据
        stocks = []
        withdraw_stocks = self.action.get_avail_withdrawals_ex()
        for s in withdraw_stocks:
            s['code'] = s['stock_code']
            s['name'] = s['stock_name']

            last_stock = s.copy()
            # 上次tick数据
            last_stock['bid_vol1'] = 100
            self.withdrawal.last_tick[last_stock['code']] = last_stock

            cur_stock = s.copy()
            # 当前tick瞬间减小幅度大于20%
            cur_stock['bid_vol1'] = 79
            stocks.append(cur_stock)

        # 配置文件设置为当买1手数减小幅度大于20%则撤单
        self.withdrawal.env.withdrawal.top.bid_vol1 = .2

        if len(stocks) > 0:
            r = measure_time(self.withdrawal.resolve, stocks)
            self.assertEqual(len(stocks), len(r))

    def test_play_sound_when_voice_msg_is_unset(self):
        stock = {'name': '美丽生态'}
        del env.withdrawal.top.voice_msg
        self.withdrawal.play_sound(stock)

    def test_play_sound_when_voice_msg_is_set(self):
        stock = {'name': '美丽生态'}
        env.withdrawal.top.voice_msg = '恭喜你，%s已经撤单成功'
        self.withdrawal.play_sound(stock)