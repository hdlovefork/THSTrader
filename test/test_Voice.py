import unittest

from THS.Voice import Voice


class TestVoice(unittest.TestCase):
    def setUp(self) -> None:
        self.voice = Voice()

    def test_say(self):
        self.voice.say("hello world")
        self.voice.say("今天天气真好")
