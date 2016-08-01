from bin.Dispatcher.Devices.Propulsion.PropulsionManager import Propulsion, NullPropulsionManager, PropulsionManager
from bin.Dispatcher.Devices.Propulsion.PropulsionManagerFactory import PropulsionManagerFactory
from bin.Dispatcher.Devices.Propulsion.PropulsionFactory import PropulsionFactory
from tests.Dispatcher.DataCreator import CreateDeviceData
from circuits import BaseComponent
from unittest.mock import MagicMock
import unittest


class TestPropulsionFactory(unittest.TestCase):
    def setUp(self):
        self.base_component = BaseComponent()
        self.data = CreateDeviceData()

    def test_creation_of_propulsion(self):
        propulsion_settings = self.data.create_propulsion_settings_entity()
        propulsion_manager_factory = PropulsionManagerFactory(self.base_component, propulsion_settings)
        propulsion_factory = PropulsionFactory(propulsion_manager_factory)
        propulsion = propulsion_factory.create()
        self.assertIsInstance(propulsion, Propulsion)

    def test_existence_of_null_propulsion_manager(self):
        propulsion_settings = self.data.create_propulsion_settings_entity()
        propulsion_manager_factory = PropulsionManagerFactory(self.base_component, propulsion_settings)
        propulsion_factory = PropulsionFactory(propulsion_manager_factory)
        propulsion = propulsion_factory.create()
        propulsion_manager = propulsion.device_manager
        self.assertIsInstance(propulsion_manager, NullPropulsionManager)

    def test_existence_of_real_propulsion_manager(self):
        propulsion_settings = self.data.create_propulsion_settings_entity()
        propulsion_manager_factory = PropulsionManagerFactory(self.base_component, propulsion_settings)
        propulsion_factory = PropulsionFactory(propulsion_manager_factory)
        propulsion_factory.device_manager_factory.port_exists = MagicMock(
            return_value=propulsion_factory.settings_entity.get_entry("port"))
        propulsion = propulsion_factory.create()
        propulsion_manager = propulsion.device_manager
        self.assertIsInstance(propulsion_manager, PropulsionManager)

if __name__ == "__main__":
    unittest.main()
