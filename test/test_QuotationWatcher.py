import unittest

from THS.QuotationWatcher import QuotationWatcher
from THS.THSQuotation import THSQuotation


class TestQuotationWatcher(unittest.TestCase):
    def setUp(self) -> None:
        self.quotation = THSQuotation('ips.toml')
        self.quotation_watcher = QuotationWatcher(self.quotation)

    def tearDown(self) -> None:
        self.quotation.close()

    def test_append_watch_stock(self):
        self.quotation_watcher.append_watch_stock([{'market_code': None, 'stock_code': None, 'stock_name': '金发拉比', 'withdraw_direct': '买入', 'withdraw_time': '16:36:43'}])
        self.assertEqual(1,len(self.quotation_watcher.watch_stocks))
        self.assertEqual([{'market_code': None, 'stock_code': None, 'stock_name': '金发拉比', 'withdraw_direct': '买入', 'withdraw_time': '16:36:43'}],self.quotation_watcher.watch_stocks)

    def test_iterate_watch_stocks(self):
        self.quotation_watcher.append_watch_stock([{'market_code': 0, 'stock_code': '002762', 'stock_name': '金发拉比', 'withdraw_direct': '买入', 'withdraw_time': '16:36:43'}])
        self.assertEqual([(0,'002762')],[(s['market_code'], s['stock_code']) for s in self.quotation_watcher.watch_stocks])

