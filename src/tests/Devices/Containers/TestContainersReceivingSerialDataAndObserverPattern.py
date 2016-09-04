import unittest
from unittest.mock import MagicMock
from bin.Devices.Containers import ContainersDevice
from bin.Devices.Containers import EventlessContainersManager


class TestContainersReceivingSerialDataAndObserverPattern(unittest.TestCase):
    def setUp(self):
        self.containers_manager = EventlessContainersManager()
        self.containers = ContainersDevice(self.containers_manager)

    def test_on_read_line_is_notify_triggered(self):
        self.containers.notify_all = MagicMock()
        self.containers_manager.on_read_line('{"test": 1}')
        self.assertTrue(self.containers.notify_all.called)


if __name__ == "__main__":
    unittest.main()
