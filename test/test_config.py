import json
import os.path
import unittest

import yaml
from dynaconf import Dynaconf

class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=['.env.toml'],
        )

    def test_can_get_serialno(self):
        self.assertEqual('127.0.0.1:62001', self.settings.serialno)

    def test_can_get_trade_top_withdraw(self):
        self.assertEqual(0.3, self.settings('trade.withdrawal.top.buy1', None))

    def test_path(self):
        print(__file__)
        print(os.path.dirname(__file__))
        print(os.path.dirname(os.path.dirname(__file__)))
        # print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

