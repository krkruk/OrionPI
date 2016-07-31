from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import Manipulator, ManipulatorManager, NullManipulatorManager
from bin.Dispatcher.Devices.Propulsion.PropulsionManager import Propulsion, PropulsionManager, NullPropulsionManager
from bin.Dispatcher.Devices.DeviceFactory import DeviceFactorySerialAbstract
from bin.Dispatcher.Devices.Propulsion.PropulsionManagerFactory import PropulsionManagerFactory
from bin.Dispatcher.Devices.Manipulator.ManipulatorManagerFactory import ManipulatorManagerFactory
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Settings.SettingsUDPEntity import SettingsUDPEntity
from bin.Dispatcher.Dictionary import SettingsKeys
from bin.Dispatcher.Dictionary import *
from bin.Settings.SettingsManager import *
from circuits import BaseComponent
from unittest.mock import MagicMock
import unittest


def add_to_dict(d, key, entry):
    d[key] = entry


class TestDeviceFactory(unittest.TestCase):
    def setUp(self):
        self.propulsion_key = SettingsKeys.PROPULSION
        self.manipulator_key = SettingsKeys.MANIPULATOR
        self.udp_key = SettingsKeys.UDP

        # key, data
        self.propulsion_serial_port = (SettingsSerialEntity.PORT, "/dev/ttyUSB0")
        self.propulsion_serial_baudrate = (SettingsSerialEntity.BAUDRATE, 115200)
        self.propulsion_serial_channel = (SettingsSerialEntity.CHANNEL, "propulsion")

        self.manipulator_serial_port = (SettingsSerialEntity.PORT, "/dev/ttyACM0")
        self.manipulator_serial_baudrate = (SettingsSerialEntity.BAUDRATE, 115200)
        self.manipulator_serial_channel = (SettingsSerialEntity.CHANNEL, "manipulator")

        self.udp_server_ip = (SettingsUDPEntity.IP, "127.0.0.1")
        self.udp_server_port = (SettingsUDPEntity.PORT, 5000)
        self.udp_server_channel = (SettingsUDPEntity.CHANNEL, "UDPServer")

        # compare
        self.propulsion_dict = {}
        add_to_dict(self.propulsion_dict, *self.propulsion_serial_port)
        add_to_dict(self.propulsion_dict, *self.propulsion_serial_baudrate)
        add_to_dict(self.propulsion_dict, *self.propulsion_serial_channel)

        self.manipulator_dict = {}
        add_to_dict(self.manipulator_dict, *self.manipulator_serial_port)
        add_to_dict(self.manipulator_dict, *self.manipulator_serial_baudrate)
        add_to_dict(self.manipulator_dict, *self.manipulator_serial_channel)

        self.udp_dict = {}
        add_to_dict(self.udp_dict, *self.udp_server_ip)
        add_to_dict(self.udp_dict, *self.udp_server_port)
        add_to_dict(self.udp_dict, *self.udp_server_channel)

        self.base_component = BaseComponent()

    def test_creation_of_null_propulsion_manager(self):
        propulsion_settings = self._create_propulsion_settings_entity()
        propulsion_manager_factory = PropulsionManagerFactory(self.base_component, propulsion_settings)
        propulsion_manager = propulsion_manager_factory.create()
        self.assertIsInstance(propulsion_manager, NullPropulsionManager)

    def test_creation_of_null_manipulator_manager(self):
        manipulator_settings = self._create_manipulator_settings_entity()
        manipulator_manager_factory = ManipulatorManagerFactory(self.base_component, manipulator_settings)
        manipulator_manager = manipulator_manager_factory.create()
        self.assertIsInstance(manipulator_manager, NullManipulatorManager)

    def test_device_factory_serial_port_exists_magic_mock_propulsion(self):
        propulsion_settings = self._create_propulsion_settings_entity()
        propulsion_factory = PropulsionManagerFactory(self.base_component, propulsion_settings)
        propulsion_factory.port_exists = MagicMock(return_value=propulsion_factory.port)
        self.assertTrue(propulsion_factory.port_exists())

    def test_creation_of_real_propulsion_manager(self):
        propulsion_settings = self._create_propulsion_settings_entity()
        propulsion_manager_factory = PropulsionManagerFactory(self.base_component, propulsion_settings)
        propulsion_manager_factory.port_exists = MagicMock(return_value=propulsion_manager_factory.port)
        propulsion_manager = propulsion_manager_factory.create()
        self.assertIsInstance(propulsion_manager, PropulsionManager)

    def test_creation_of_real_manipulator_manager(self):
        manipulator_settings = self._create_manipulator_settings_entity()
        manipulator_manager_factory = ManipulatorManagerFactory(self.base_component, manipulator_settings)
        manipulator_manager_factory.port_exists = MagicMock(return_value=manipulator_manager_factory.port)
        manipulator_manager = manipulator_manager_factory.create()
        self.assertIsInstance(manipulator_manager, ManipulatorManager)

    def _create_propulsion_settings_entity(self):
        propulsion = SettingsSerialEntity(key=self.propulsion_key)
        propulsion.add_entries(self.propulsion_dict)
        return propulsion

    def _create_manipulator_settings_entity(self):
        manipulator = SettingsSerialEntity(key=self.manipulator_key)
        manipulator.add_entries(self.manipulator_dict)
        return manipulator

if __name__ == "__main__":
    unittest.main()
