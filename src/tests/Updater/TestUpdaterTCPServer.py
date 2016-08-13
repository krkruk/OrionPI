from bin.Updater.UpdaterTCPServer import *
from bin.Updater.DataAssembly import DataAssembly
from bin.Updater.UpdaterTransmissionNegotiation import TransmissionNegotiation
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
        self.syn = json.dumps(self.positive_sync_dict).encode("ascii")

    def test_on_read_send_init_syn(self):
        self.eventless_server.on_read(self.raddr, self.syn)
        self.assertEqual(self.eventless_server.mode, EventlessUpdaterTCPServer.MODE.GET_DATA)


if __name__ == "__main__":
    unittest.main()
