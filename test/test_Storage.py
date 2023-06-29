import unittest

from THS.Storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = Storage()

    def test_set(self):
        self.storage.set('张家界',('000430',0))
        self.storage.set('美丽生态',('000431',0))
        self.assertEqual(('000430',0), self.storage.get('张家界'))
        self.assertEqual(('000431',0), self.storage.get('美丽生态'))
        code,market = self.storage.get('美丽生态')
        self.assertEqual('000431',code)
        self.assertEqual(0,market)

    def test_has(self):
        self.storage.set('test', 'test')
        self.assertTrue(self.storage.has('test'))

    def test_get(self):
        self.storage.set('test', 'test')
        self.assertEqual('test', self.storage.get('test'))

    def test_delete(self):
        self.storage.set('test', 'test')
        self.storage.remove('test')
        self.assertFalse(self.storage.has('test'))

    def test_clear(self):
        self.storage.set('test', 'test')
        self.storage.clear()
        self.assertFalse(self.storage.has('test'))

