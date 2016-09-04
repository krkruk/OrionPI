from tests.Dispatcher.DataCreator import CreateDeviceData
from bin.Devices.Manipulator import Manipulator
from bin.Devices.Propulsion import Propulsion
from bin.Devices.Containers import ContainersDevice
from bin.Devices import DeviceWholesale
from bin.Dispatcher.Dictionary import *
from circuits import BaseComponent
import unittest


class TestDeviceGrossSeller(unittest.TestCase):
    def setUp(self):
        self.data = CreateDeviceData()
        self.propulsion_settings_entity = self.data.create_propulsion_settings_entity()
        self.manipulator_settings_entity = self.data.create_manipulator_settings_entity()
        self.containers_settings_entity = self.data.create_containers_settings_entity()
        self.base_component = BaseComponent()

    def test_creation_of_propulsion(self):
        wholesaler = DeviceWholesale(self.base_component, [self.propulsion_settings_entity])
        propulsion = wholesaler.sell(SettingsKeys.PROPULSION)
        self.assertIsInstance(propulsion, Propulsion)

    def test_creation_of_manipulator(self):
        wholesaler = DeviceWholesale(self.base_component, [self.manipulator_settings_entity])
        manipulator = wholesaler.sell(SettingsKeys.MANIPULATOR)
        self.assertIsInstance(manipulator, Manipulator)

    def test_creation_of_containers(self):
        wholesaler = DeviceWholesale(self.base_component, [self.containers_settings_entity])
        containers = wholesaler.sell(SettingsKeys.CONTAINERS)
        self.assertIsInstance(containers, ContainersDevice)

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
                                      self.manipulator_settings_entity,
                                      self.containers_settings_entity])
        all_devices = wholesaler.sell_all()
        self.assertEqual(3, len(all_devices))


if __name__ == "__main__":
    unittest.main()
