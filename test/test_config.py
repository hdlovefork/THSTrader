import json
import os.path
import unittest

from dynaconf import Dynaconf

from THS.THSWithdrawal import THSWithdrawal


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=['.env.toml'],
        )

    def test_can_get_serial_no(self):
        self.assertEqual('2623729', self.settings.serial_no)

    def test_can_get_trade_top_withdraw(self):
        self.assertEqual(0.3, self.settings('withdrawal.top.bid_vol1', None))
        self.assertEqual(THSWithdrawal.DIRECT_INSENSITIVE, self.settings('withdrawal.top.direct_sensitive',THSWithdrawal.DIRECT_INSENSITIVE))

    def test_path(self):
        print(__file__)
        print(os.path.dirname(__file__))
        print(os.path.dirname(os.path.dirname(__file__)))
        # print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

