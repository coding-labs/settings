from settings import Settings
import unittest

class SettingsTest(unittest.TestCase):
    def setUp(self):
        self.settings = Settings(max_filesize=100)

    def tearDown(self):
        pass

    def equal(self, setting, key, value):
        self.settings.loads(setting)
        self.assertEqual(self.settings[key], value)

    def error(self, setting, error_type):
        with self.assertRaises(error_type):
            self.settings.loads(setting)

    def test_numeric(self):
        self.equal("test=1", 'test', 1)

    def test_negative_number(self):
        self.equal(" num = -65498 ", "num", -65498)

    def test_invalid_numeric(self):
        self.error("num = 1.2.3", ValueError)

    def test_key_error(self):
        self.error("@key = 6", KeyError)

if __name__=='__main__':
    unittest.main()
