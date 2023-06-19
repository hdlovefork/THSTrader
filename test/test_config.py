import unittest


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        from script.config import Config
        self.config = Config('../config.yaml')

    def test_can_get_serialno(self):
        self.assertEqual(self.config.serialno, 'emulator-5554')
