from bin.Updater.UpdaterDataProcessor import UpdaterDataProcessor
from unittest.mock import patch
import unittest


class TestUpdaterDataProcessor(unittest.TestCase):
    def setUp(self):
        self.data_processor = UpdaterDataProcessor()
        self.random_data = b"random binary data in bytes :D"

    def test_process_data_acquire_it(self):
        self.data_processor.process(self.random_data)
        self.assertEqual(self.random_data, self.data_processor.raw_data)

    @patch("builtins.open")
    def test_save_data(self, mock_open):
        self.data_processor.process(self.random_data)
        self.data_processor.save("file.txt")
        self.assertTrue(mock_open.called)


if __name__ == "__main__":
    unittest.main()
