import json
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

