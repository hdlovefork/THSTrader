import os
import unittest

import toml

from THS.THSQuotation import THSQuotation, load_ips


class TestTHSQuotation(unittest.TestCase):
    def setUp(self) -> None:
        self.quotation = THSQuotation(os.path.join('../','bin', 'ips.toml'))

    def test_get_xdxr_info(self):
        print(self.quotation.get_xdxr_info(0, '000001'))

    def test_get_security_quotes(self):
        print(self.quotation.get_security_quotes([(0, '000001')]))

    def test_load_ips(self):
        with open('ips.toml', 'r') as f:
            config = toml.load(f)
            f.close()
            self.assertEqual([["218.6.170.47", "7709", ], ["123.125.108.14", "7709", ], ], config['ips'])

    def test_load_str(self):
        _str = 'ips = [ [ "218.6.170.47", "7709",], [ "123.125.108.14", "7709",],]'
        config = toml.loads(_str)
        self.assertEqual([["218.6.170.47", "7709", ], ["123.125.108.14", "7709", ], ], config['ips'])
