from settings import Settings
import unittest

class SettingsTest(unittest.TestCase):
    def setUp(self):
        self.settings = Settings(max_filesize=100)

    def tearDown(self):
        pass

    def test_numeric(self):
        setting = "test=1"
        self.settings.loads(setting)
        self.assertEqual(self.settings["test"], 1)

    def test_invalid_numeric(self):
        setting = "num = 1.2.3"
        with self.assertRaises(ValueError):
            self.settings.loads(setting)

    def test_key_error(self):
        setting = "@key = 6"
        with self.assertRaises(KeyError):
            self.settings.loads(setting)

if __name__=='__main__':
    unittest.main()
