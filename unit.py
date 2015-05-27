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
        self.equal(" num = -65536 ", "num", -65536)

    def test_invalid_numeric(self):
        self.error("num = 1.2.3", ValueError)

    def test_key_error(self):
        self.error("@key = 6", KeyError)

    def test_comment(self):
        setting = "#comment here"
        self.settings.loads(setting)
        self.assertEqual(self.settings.has_key(setting), False)

    def test_string(self):
        self.equal("str=\'ok my man!\'", "str", "ok my man!")

    def test_empty_settings(self):
        self.equal('empty=', 'empty', None)

    def test_empty_lines(self):
        setting = "line1=\"ok\"\n \t \nline2=1.0"
        self.settings.loads(setting)
        self.assertEqual(self.settings['line1'],"ok")
        self.assertEqual(self.settings['line2'], 1.0)

if __name__=='__main__':
    unittest.main()
