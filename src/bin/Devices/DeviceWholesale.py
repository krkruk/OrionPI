from bin.Devices.Manipulator.ManipulatorFactory import ManipulatorFactory, ManipulatorManagerFactory
from bin.Devices.Propulsion.PropulsionFactory import PropulsionFactory, PropulsionManagerFactory
from bin.Devices.DeviceFactory import DeviceFactoryAbstract
from bin.Dispatcher.Dictionary import SettingsKeys
from bin.Devices.DeviceAbstract import NullDevice


class DeviceWholesaleAbstract:
    def sell(self, device_name):
        raise NotImplemented()

    def sell_all(self):
        raise NotImplemented()


class _CreateDevice:
    def __init__(self, DeviceFactory, DeviceManagerFactory):
        assert issubclass(DeviceFactory, DeviceFactoryAbstract)
        assert issubclass(DeviceManagerFactory, DeviceFactoryAbstract)
        self.DeviceFactory = DeviceFactory
        self.DeviceManagerFactory = DeviceManagerFactory

    def create_device(self, base_component, device_settings_entities):
        if device_settings_entities:
            device_settings_entity = device_settings_entities.pop(0)
            return self.DeviceFactory(self.DeviceManagerFactory(
                base_component, device_settings_entity
            )).create()
        else:
            return NullDevice()


class DeviceWholesale(DeviceWholesaleAbstract):
    def __init__(self, base_component, settings_entity_list_of_devices):
        assert isinstance(settings_entity_list_of_devices, list)
        self.settings_of_devices = settings_entity_list_of_devices
        self.base_component = base_component
        self._propulsion_factory = _CreateDevice(PropulsionFactory, PropulsionManagerFactory)
        self._manipulator_factory = _CreateDevice(ManipulatorFactory, ManipulatorManagerFactory)
        self.available_products = [
            SettingsKeys.PROPULSION,
            SettingsKeys.MANIPULATOR,
            SettingsKeys.CONTAINERS
        ]

    def sell(self, device_name):
        if device_name == SettingsKeys.PROPULSION:
            return self._create_propulsion()
        elif device_name == SettingsKeys.MANIPULATOR:
            return self._create_manipulator()
        elif device_name == SettingsKeys.CONTAINERS:
            return
        else:
            return NullDevice()

    def sell_all(self):
        return [self.sell(device_name) for device_name in self.available_products
                if device_name != SettingsKeys.CONTAINERS]

    def _create_propulsion(self):
        propulsion_settings = self._find_device_settings_entity(SettingsKeys.PROPULSION)
        return self._propulsion_factory.create_device(
            self.base_component, propulsion_settings)

    def _create_manipulator(self):
        manipulator_settings = self._find_device_settings_entity(SettingsKeys.MANIPULATOR)
        return self._manipulator_factory.create_device(
            self.base_component, manipulator_settings)

    def _find_device_settings_entity(self, device_name):
        return [device for device in self.settings_of_devices
                if device.key == device_name]
