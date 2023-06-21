import unittest
import uiautomator2 as u2
from test import env


class TestOCR(unittest.TestCase):
    def setUp(self) -> None:
        self.d = u2.connect_usb(env.serialno)

    def test_withdraw_click(self):
        self.d.xpath('//*[@content-desc="交易"]/android.widget.ImageView[1]').click()

    def test_dump(self):
        print(self.d.dump_hierarchy())

