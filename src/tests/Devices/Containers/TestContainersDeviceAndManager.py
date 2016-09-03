import json
import unittest
from bin.Devices.Containers.ContainersDevice import ContainersDevice
from bin.Devices.Containers.ContainersManager import EventlessContainersManager, NullContainersManager


class TestContainerDeviceDataFlow(unittest.TestCase):
    def setUp(self):
        self.eventless_mgr = EventlessContainersManager()
        self.null_mgr = NullContainersManager()
        self.sample_data = {"sample": "data"}

    def test_eventless_data_flow(self):
        container = ContainersDevice(self.eventless_mgr)
        container.update_data(self.sample_data)
        self.assertDictEqual(self.sample_data, json.loads(self.eventless_mgr.line_sent))


if __name__ == "__main__":
    unittest.main()
