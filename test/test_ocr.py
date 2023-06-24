import unittest
import uiautomator2 as u2

from THS.THSTrader import THSTrader
from main import env


class TestOCR(unittest.TestCase):
    def setUp(self) -> None:
        self.d = u2.connect_usb(env.serialno)

    def test_withdraw_click(self):
        self.d.xpath('//*[@content-desc="交易"]/android.widget.ImageView[1]').click()

    def test_dump(self):
        print(self.d.dump_hierarchy())

    def test_view_stock_code(self):
        root = lambda: self.d.xpath('@com.hexin.plat.android:id/chedan_recycler_view')
        root().child(f'android.widget.LinearLayout[{0 + 1}]').click()
        if self.d.xpath('@com.hexin.plat.android:id/stockcode_textview').wait(1):
            print(self.d.xpath('@com.hexin.plat.android:id/stockcode_textview').get_text())
            self.d.xpath('@com.hexin.plat.android:id/option_cancel').click()

    def test_find_other_bar(self):
        root = lambda: self.d.xpath('@com.hexin.plat.android:id/chedan_recycler_view')

        print(len(root().child('*').all()))
        print(root().child('*[3]').info)
        # 存在其它按钮
        print(root().child('*[3]').child('*[@resource-id="com.hexin.plat.android:id/cannot_chedan_title_text"]').exists)

    def test_in_withdrawal_page(self):
        print(self.d(resourceId="com.hexin.plat.android:id/chedan_recycler_view").exists)