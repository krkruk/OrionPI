from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import Manipulator
from tests.Dispatcher.DataCreator import CreateDeviceData
from bin.Dispatcher.Devices.DeviceWholesale import DeviceWholesale
from bin.Dispatcher.Dictionary import *
from bin.Dispatcher.Devices.Propulsion.PropulsionManager import Propulsion
from circuits import BaseComponent
import unittest


class TestDeviceGrossSeller(unittest.TestCase):
    def setUp(self):
        self.data = CreateDeviceData()
        self.propulsion_settings_entity = self.data.create_propulsion_settings_entity()
        self.manipulator_settings_entity = self.data.create_manipulator_settings_entity()
        self.base_component = BaseComponent()

    def test_creation_of_propulsion(self):
        wholesaler = DeviceWholesale(self.base_component, [self.propulsion_settings_entity])
        propulsion = wholesaler.sell(SettingsKeys.PROPULSION)
        self.assertIsInstance(propulsion, Propulsion)

    def test_creation_of_manipulator(self):
        wholesaler = DeviceWholesale(self.base_component, [self.manipulator_settings_entity])
        manipulator = wholesaler.sell(SettingsKeys.MANIPULATOR)
        self.assertIsInstance(manipulator, Manipulator)

    def test_creation_of_propulsion_when_no_propulsion_settings_entity_given(self):
        wholesaler = DeviceWholesale(self.base_component, [self.manipulator_settings_entity])
        propulsion = wholesaler.sell(SettingsKeys.PROPULSION)
        self.assertFalse(propulsion)

    def test_creation_of_manipulator_when_no_propulsion_settings_entity_given(self):
        wholesaler = DeviceWholesale(self.base_component, [])
        manipulator = wholesaler.sell(SettingsKeys.MANIPULATOR)
        self.assertFalse(manipulator)

    def test_creation_of_all_available_products(self):
        wholesaler = DeviceWholesale(self.base_component,
                                     [self.propulsion_settings_entity,
                                      self.manipulator_settings_entity])
        all_devices = wholesaler.sell_all()
        self.assertEqual(2, len(all_devices))


if __name__ == "__main__":
    unittest.main()