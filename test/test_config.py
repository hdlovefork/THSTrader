import json
import os.path
import unittest

import yaml
from dynaconf import Dynaconf

class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        with open('config.yaml', 'r') as file:
            # 使用 yaml.load 方法将文件内容转换为 Python 对象
            self.yarm_config = yaml.load(file, Loader=yaml.FullLoader)
        with open('config.json') as f:
            self.json_config = json.load(f)

        self.settings = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=['config.toml'],
        )

    def test_can_get_serialno(self):
        self.assertEqual(self.yarm_config['serialno'], 'emulator-5554')
        self.assertEqual(self.json_config['serialno'], 'emulator-5554')
        self.assertEqual(self.settings.serialno, 'emulator-5554')

    def test_can_get_trade_top_withdraw(self):
        self.assertEqual(0.3, self.yarm_config['trade']['top']['withdraw'])
        self.assertEqual(0.3, self.json_config['trade']['top']['withdraw'])
        self.assertEqual(0.3, self.settings('trade.top.withdraw', None))
        self.assertEqual(0.3, self.settings.get('trade.top.withdraw', None))

    def test_path(self):
        print(__file__)
        print(os.path.dirname(__file__))
        print(os.path.dirname(os.path.dirname(__file__)))
        # print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


    def test_ips(self):
        settings = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=['ips.toml'],
        )
        self.assertEqual(["218.6.170.47", 7709], settings.ips[0])
        self.assertEqual(["123.125.108.14", 7709], settings.ips[1])

