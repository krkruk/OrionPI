from bin.Updater.Updater import UpdaterZIP, Updater
from unittest.mock import patch, MagicMock
import unittest
import pathlib
import os


class TestUpdaterZIP(unittest.TestCase):
    def setUp(self):
        self.filename = "update_fake.zip"
        self.zip = UpdaterZIP("update_fake.zip")

    def test_update_file_exists(self):
        self.assertFalse(self.zip.check_file_exists())

    @patch("zipfile.is_zipfile")
    def test_is_zip_file(self, mock_is_zip):
        self.zip.check_file_properties()
        mock_is_zip.assert_called_with(self.filename)

    @patch("os.remove")
    def test_file_remove(self, mock_remove):
        self.zip.check_file_exists = MagicMock(return_value=True)
        self.zip.erase_update_file()
        mock_remove.assert_called_with(self.filename)

    def test_can_decompress_file(self):
        self.zip.check_file_exists = MagicMock(return_value=True)
        self.zip.check_file_properties = MagicMock(return_value=True)
        self.assertTrue(self.zip._can_decompress_file())

    @unittest.skipUnless(__name__ == "TestUpdater", "Do not create file during global testing")
    def test_real_zip_file(self):
        zip_algorithm = UpdaterZIP("test.zip")
        self.assertTrue(zip_algorithm.decompress())
        if pathlib.Path("text.txt").is_file():
            os.remove("text.txt")


class TestUpdaterAtZIPAlgorithm(unittest.TestCase):
    def setUp(self):
        self.filename = "update_fake.zip"
        self.zip = UpdaterZIP("update_fake.zip")
        self.updater = Updater(self.zip)
        self.zip.decompress = MagicMock()
        self.zip.erase_update_file = MagicMock()

    def test_update(self):
        self.updater.update()
        self.assertTrue(self.zip.decompress.called)

    def test_clear_update_file(self):
        self.updater.clear_update_file()
        self.assertTrue(self.zip.erase_update_file.called)

if __name__ == '__main__':
    unittest.main()
