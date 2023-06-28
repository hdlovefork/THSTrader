import unittest


class TestPositionStocks(unittest.TestCase):
    def setUp(self) -> None:
        self.ps = []

    def test_append(self):
        self.ps.extend([{'stock_code': '600072', 'market_code': 1, 'stock_name': '中船科技', 'withdraw_time': '10:19:39', 'withdraw_direct': '买入'},
{'stock_code': '000600', 'market_code': 0, 'stock_name': '建投能源', 'withdraw_time': '10:17:58', 'withdraw_direct': '买入'}])
        print(self.ps)

    def test_remove(self):
        self.ps.extend([{'stock_code': '600072', 'market_code': 1, 'stock_name': '中船科技',
                         'withdraw_time': '10:19:39', 'withdraw_direct': '买入'},
                        {'stock_code': '000600', 'market_code': 0, 'stock_name': '建投能源',
                         'withdraw_time': '10:17:58', 'withdraw_direct': '买入'}])
        self.assertEqual([{'stock_code': '600072', 'market_code': 1, 'stock_name': '中船科技',
                         'withdraw_time': '10:19:39', 'withdraw_direct': '买入'},
                        {'stock_code': '000600', 'market_code': 0, 'stock_name': '建投能源',
                         'withdraw_time': '10:17:58', 'withdraw_direct': '买入'}],self.ps)

        self.ps.remove({'stock_code': '600072', 'market_code': 1, 'stock_name': '中船科技',
                         'withdraw_time': '10:19:39', 'withdraw_direct': '买入'})
        self.assertEqual([{'stock_code': '000600', 'market_code': 0, 'stock_name': '建投能源',
                         'withdraw_time': '10:17:58', 'withdraw_direct': '买入'}],self.ps)

