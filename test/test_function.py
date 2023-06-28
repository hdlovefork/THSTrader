import unittest

from THS.__ini__ import calc_insert_stocks, calc_delete_stocks


class TestFunction(unittest.TestCase):
    def test_calc_insert_stock(self):
        r = calc_insert_stocks([
            {'股票代码': None, '股票名称': '建投能源', '委托价格': 6.94, '委托数量': 400, '委托方向': '买入','委托状态': '未成交'}
        ], [
            {'股票代码': None, '股票名称': '建投能源', '委托价格': 6.94, '委托数量': 400, '委托方向': '买入','委托状态': '未成交'},
            {'股票代码': None, '股票名称': '奥园美谷', '委托价格': 6.94, '委托数量': 400, '委托方向': '买入','委托状态': '未成交'},
        ])
        self.assertEqual([{'股票代码': None, '股票名称': '奥园美谷', '委托价格': 6.94, '委托数量': 400, '委托方向': '买入','委托状态': '未成交'}], r)

        r = calc_insert_stocks([
            {'stock_code': '002762', 'market_code': 0, 'stock_name': '金发拉比', 'withdraw_time': '16:55:26',
             'withdraw_direct': '买入'}
        ], [
            {'stock_code': '002762', 'market_code': 0, 'stock_name': '金发拉比', 'withdraw_time': '16:56:26',
             'withdraw_direct': '买入'},
            {'stock_code': '002762', 'market_code': 0, 'stock_name': '金发拉比', 'withdraw_time': '16:55:26',
             'withdraw_direct': '买入'},
        ])
        self.assertEqual([
            {'stock_code': '002762', 'market_code': 0, 'stock_name': '金发拉比', 'withdraw_time': '16:56:26',
             'withdraw_direct': '买入'}
        ], r)

    def test_calc_delete_stock(self):
        r = calc_delete_stocks([
            {'股票代码': None, '股票名称': '建投能源', '委托价格': 6.94, '委托数量': 400, '委托方向': '买入','委托状态': '未成交'},
            {'股票代码': None, '股票名称': '奥园美谷', '委托价格': 6.94, '委托数量': 400, '委托方向': '买入','委托状态': '未成交'},
        ], [
            {'股票代码': None, '股票名称': '建投能源', '委托价格': 6.94, '委托数量': 400, '委托方向': '买入','委托状态': '未成交'},
        ])
        self.assertEqual([{'股票代码': None, '股票名称': '奥园美谷', '委托价格': 6.94, '委托数量': 400, '委托方向': '买入','委托状态': '未成交'}], r)