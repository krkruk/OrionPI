from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import Manipulator, EventlessManipulatorManager, NullManipulatorManager
from bin.Dispatcher.Devices.Propulsion.PropulsionManager import Propulsion, EventlessPropulsionManager, NullPropulsionManager
from bin.Dispatcher.Devices.DeviceFactory import DeviceFactory
from bin.Dispatcher.Dictionary import SettingsKeys
import unittest


class TestDeviceFactory(unittest.TestCase):
    def setUp(self):
        pass

    def test_creation_of_null_propulsion(self):
        factory = DeviceFactory()
        propulsion = factory.create(SettingsKeys.PROPULSION)
        self.assertIsInstance(propulsion, NullPropulsionManager)

    def test_creation_of_null_manipulator(self):
        factory = DeviceFactory()
        manipulator = factory.create(SettingsKeys.MANIPULATOR)
        self.assertIsInstance(manipulator, NullManipulatorManager)

if __name__ == "__main__":
    unittest.main()
