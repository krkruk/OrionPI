from bin.Dispatcher.Devices.Manipulator.ManipulatorFactory import ManipulatorFactory, ManipulatorManagerFactory
from bin.Dispatcher.Devices.Propulsion.PropulsionFactory import PropulsionFactory, PropulsionManagerFactory
from bin.Dispatcher.Devices.DeviceAbstract import NullDevice
from bin.Dispatcher.Dictionary import SettingsKeys


class DeviceWholesaleAbstract:
    def sell(self, device_name):
        raise NotImplemented()

    def sell_all(self):
        raise NotImplemented()


class DeviceWholesale(DeviceWholesaleAbstract):
    def __init__(self, base_component, settings_entity_list_of_devices):
        assert isinstance(settings_entity_list_of_devices, list)
        self.settings_of_devices = settings_entity_list_of_devices
        self.base_component = base_component
        self.available_products = [
            SettingsKeys.PROPULSION,
            SettingsKeys.MANIPULATOR,
            SettingsKeys.PERIPHERIES
        ]

    def sell(self, device_name):
        if device_name == SettingsKeys.PROPULSION:
            return self._create_propulsion()
        elif device_name == SettingsKeys.MANIPULATOR:
            return self._create_manipulator()
        elif device_name == SettingsKeys.PERIPHERIES:
            return
        else:
            return NullDevice()

    def sell_all(self):
        return [self.sell(device_name) for device_name in self.available_products
                if device_name != SettingsKeys.PERIPHERIES]

    def _create_propulsion(self):
        propulsion_settings = self._find_device_settings_entity(SettingsKeys.PROPULSION)
        if propulsion_settings:
            propulsion_settings_entity = propulsion_settings.pop(0)
            return PropulsionFactory(PropulsionManagerFactory(
                self.base_component, propulsion_settings_entity)).create()
        else:
            return NullDevice()

    def _create_manipulator(self):
        manipulator_settings = self._find_device_settings_entity(SettingsKeys.MANIPULATOR)

        if manipulator_settings:
            manipulator_settings_entity = manipulator_settings.pop(0)
            return ManipulatorFactory(ManipulatorManagerFactory(
                self.base_component, manipulator_settings_entity)).create()
        else:
            return NullDevice()

    def _find_device_settings_entity(self, device_name):
        return [device for device in self.settings_of_devices
                if device.key == device_name]
