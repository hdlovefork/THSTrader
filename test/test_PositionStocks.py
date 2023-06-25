import unittest

from script.PositionStocks import PositionStocks


class TestPositionStocks(unittest.TestCase):
    def test_append(self):
        ps = PositionStocks()
        ps.append((('0', '000001'), ('0', '000002')))
        print(ps.to_quot_list())