import unittest
from unittest.mock import MagicMock
from bin.Devices.Propulsion import Propulsion
from bin.Devices.Propulsion import EventlessPropulsionManager


class TestContainersReceivingSerialDataAndObserverPattern(unittest.TestCase):
    def setUp(self):
        self.propulsion_manager = EventlessPropulsionManager()
        self.propulsion = Propulsion(self.propulsion_manager)

    def test_on_read_line_is_notify_triggered(self):
        self.propulsion.notify_all = MagicMock()
        self.propulsion_manager.on_read_line('{"test": 1}')
        self.assertTrue(self.propulsion.notify_all.called)


if __name__ == "__main__":
    unittest.main()
