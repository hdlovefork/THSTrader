import os
import unittest

import toml

from THS.THSQuotation import THSQuotation


class TestTHSQuotation(unittest.TestCase):
    def setUp(self) -> None:
        self.quotation = THSQuotation(os.path.join('../','bin', 'ips.toml'))

    def test_get_xdxr_info(self):
        print(self.quotation.get_security_quotes(1, '601177'))

    def test_get_security_quotes(self):
        stocks = [{'stock_code': '600072', 'market_code': 1, 'stock_name': '中船科技', 'withdraw_time': '10:19:39', 'withdraw_direct': '买入'},
{'stock_code': '000600', 'market_code': 0, 'stock_name': '建投能源', 'withdraw_time': '10:17:58', 'withdraw_direct': '买入'}]
        for v in self.quotation.get_security_quotes(tuple((v['market_code'], v['stock_code']) for v in stocks)):
            print(v)

    def test_load_ips(self):
        with open('ips.toml', 'r') as f:
            config = toml.load(f)
            f.close()
            self.assertEqual([["218.6.170.47", "7709", ], ["123.125.108.14", "7709", ], ], config['ips'])

    def test_load_str(self):
        _str = 'ips = [ [ "218.6.170.47", "7709",], [ "123.125.108.14", "7709",],]'
        config = toml.loads(_str)
        self.assertEqual([["218.6.170.47", "7709", ], ["123.125.108.14", "7709", ], ], config['ips'])
