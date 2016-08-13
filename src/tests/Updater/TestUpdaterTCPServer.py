from bin.Updater.FileTransferProtocol import FileTransferProtocol as FTP
from bin.Updater.UpdaterTCPServer import *
from bin.Updater.DataAssembly import DataAssembly
from bin.Updater.UpdaterTransmissionNegotiation import TransmissionNegotiation
from unittest.mock import MagicMock, Mock, call
import unittest
import hashlib
import json


class TestUpdaterTCPServer(unittest.TestCase):
    def setUp(self):
        self.bind = ("127.0.0.1", 5000)
        self.raddr = ("127.0.0.1", 6000)
        self.negotiator = TransmissionNegotiation()
        self.data_assembly = DataAssembly()
        self.eventless_server = EventlessUpdaterTCPServer(self.bind, self.negotiator, self.data_assembly)
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
        self.eventless_server.on_read(self.raddr, self.syn)
        self.assertEqual(self.eventless_server.ftp.mode, FTP.MODE.GET_DATA)

    def test_all_collecting_data_steps_succeeds_on_processing_data_changed_mode_to_negotiate(self):
        self.eventless_server.ftp._process_recvd_data = MagicMock()
        self.eventless_server.on_read(self.raddr, self.syn)
        self.eventless_server.on_read(self.raddr, self.data_example)
        self.assertTrue(self.eventless_server.ftp._process_recvd_data.called)

    def test_too_much_data_sent_to_buffer(self):
        self.eventless_server.ftp._handle_error = MagicMock()
        self.eventless_server.on_read(self.raddr, self.syn)
        self._double_the_size_of_recvd_bytes()
        self.eventless_server.on_read(self.raddr, self.data_example)
        self.assertTrue(self.eventless_server.ftp._handle_error.called)

    def _double_the_size_of_recvd_bytes(self):
        self.eventless_server.ftp.data_assembly.append_bytes(self.data_example)
        self.eventless_server.ftp.data_assembly.append_bytes(self.data_example)


if __name__ == "__main__":
    unittest.main()
