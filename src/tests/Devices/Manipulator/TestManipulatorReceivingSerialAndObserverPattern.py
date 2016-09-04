import unittest
from unittest.mock import MagicMock
from bin.Devices.Manipulator import Manipulator
from bin.Devices.Manipulator import EventlessManipulatorManager


class TestContainersReceivingSerialDataAndObserverPattern(unittest.TestCase):
    def setUp(self):
        self.manipulator_manager = EventlessManipulatorManager()
        self.manipulator = Manipulator(self.manipulator_manager)

    def test_on_read_line_is_notify_triggered(self):
        self.manipulator.notify_all = MagicMock()
        self.manipulator_manager.on_read_line('{"test": 1}')
        self.assertTrue(self.manipulator.notify_all.called)


if __name__ == "__main__":
    unittest.main()
