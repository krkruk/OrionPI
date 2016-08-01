from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import NullManipulatorManager, ManipulatorManager, Manipulator
from bin.Dispatcher.Devices.Manipulator.ManipulatorManagerFactory import ManipulatorManagerFactory
from bin.Dispatcher.Devices.Manipulator.ManipulatorFactory import ManipulatorFactory
from tests.Dispatcher.DataCreator import CreateDeviceData
from circuits import BaseComponent
from unittest.mock import MagicMock
import unittest


class TestManipulatorFactory(unittest.TestCase):
    def setUp(self):
        self.base_component = BaseComponent()
        self.data = CreateDeviceData()

    def test_creation_of_manipulator(self):
        manipulator_settings = self.data.create_manipulator_settings_entity()
        manipulator_manager_factory = ManipulatorManagerFactory(self.base_component, manipulator_settings)
        manipulator = ManipulatorFactory(manipulator_manager_factory).create()
        self.assertIsInstance(manipulator, Manipulator)

    def test_existence_of_null_manipulator_manager(self):
        manipulator_settings = self.data.create_manipulator_settings_entity()
        manipulator_manager_factory = ManipulatorManagerFactory(self.base_component, manipulator_settings)
        manipulator = ManipulatorFactory(manipulator_manager_factory).create()
        manipulator_manager = manipulator.device_manager
        self.assertIsInstance(manipulator_manager, NullManipulatorManager)

    def test_existence_of_real_manipulator_manager(self):
        manipulator_settings = self.data.create_manipulator_settings_entity()
        manipulator_manager_factory = ManipulatorManagerFactory(self.base_component, manipulator_settings)
        manipulator_factory = ManipulatorFactory(manipulator_manager_factory)
        manipulator_factory.device_manager_factory.port_exists = MagicMock(
            return_value=manipulator_factory.device_manager_factory.settings_entity.get_entry("port"))
        manipulator = manipulator_factory.create()
        manipulator_manager = manipulator.device_manager
        self.assertIsInstance(manipulator_manager, ManipulatorManager)


if __name__ == "__main__":
    unittest.main()
