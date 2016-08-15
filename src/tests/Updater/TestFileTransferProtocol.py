from bin.Updater.FileTransferProtocol import *
from bin.Updater.DataAssembly import DataAssembly
from unittest.mock import MagicMock
from bin.Updater.UpdaterDataProcessor import UpdaterDataProcessor
import unittest
import hashlib

FTP = FileTransferProtocol


class TestFileTransferProtocol(unittest.TestCase):
    def setUp(self):
        self.bind = ("127.0.0.1", 5000)
        self.raddr = ("127.0.0.1", 6000)
        self.negotiator = TransmissionNegotiation()
        self.data_assembly = DataAssembly()
        self.data_processor = UpdaterDataProcessor()
        self.data_processor._save_data = MagicMock()
        self.ftp_algorithm = FileTransferProtocol(self.negotiator,
                                                  self.data_assembly,
                                                  self.data_processor)
        self.data_example = b"mydata_test   some random text"
        self.data_md5 = hashlib.md5(self.data_example).hexdigest()
        self.positive_sync_dict = {
            "SYN": {
                "filename": "update.zip",
                "filesize": len(self.data_example),
                "MD5": self.data_md5
            }
        }
        self.positive_ack_dict = {
            "ACK": {
                "filename": "update.zip",
                "filesize": len(self.data_example),
                "MD5": self.data_md5
            }
        }
        self.syn = json.dumps(self.positive_sync_dict).encode("ascii") + b"\r\n"

    def test_on_read_send_init_syn(self):
        self.ftp_algorithm.run(self.syn)
        self.assertEqual(self.ftp_algorithm.mode, FTP.MODE.GET_DATA)

    def test_write_line_on_correct_data_sent(self):
        self.ftp_algorithm.stdio = MagicMock()
        self.ftp_algorithm.negotiate(self.syn)
        self.assertTrue(self.ftp_algorithm.stdio.called)

    def test_assemble_data(self):
        self.ftp_algorithm._process_recvd_data = MagicMock()
        self.ftp_algorithm.negotiate(self.syn)
        self.ftp_algorithm.assemble_data(self.data_example)
        self.assertTrue(self.ftp_algorithm._process_recvd_data.called)

    def test_return_to_negotiation_mode_after_processing_data(self):
        self.ftp_algorithm.negotiate(self.syn)
        self.ftp_algorithm.assemble_data(self.data_example)
        self.assertEqual(self.ftp_algorithm.mode, FTP.MODE.NEGOTIATE)

    def test_all_collecting_data_steps_succeeds_on_processing_data_changed_mode_to_negotiate(self):
        self.ftp_algorithm._process_recvd_data = MagicMock()
        self.ftp_algorithm.run(self.syn)
        self.ftp_algorithm.run(self.data_example)
        self.assertTrue(self.ftp_algorithm._process_recvd_data.called)

    def test_too_much_data_sent_to_buffer(self):
        self.ftp_algorithm.stderr = MagicMock()
        self.ftp_algorithm.run(self.syn)
        self._double_the_size_of_recvd_bytes()
        self.ftp_algorithm.run(self.data_example)
        self.assertTrue(self.ftp_algorithm.stderr.called)

    def test_on_error_handling(self):
        self.ftp_algorithm.stderr = MagicMock()
        self.ftp_algorithm._handle_error("error - big one!")
        self.assertTrue(self.ftp_algorithm.stderr.called)

    def _double_the_size_of_recvd_bytes(self):
        self.ftp_algorithm.data_assembly.append_bytes(self.data_example)
        self.ftp_algorithm.data_assembly.append_bytes(self.data_example)

if __name__ == "__main__":
    unittest.main()
