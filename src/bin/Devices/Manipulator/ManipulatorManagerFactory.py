from bin.Devices.Manipulator import NullManipulatorManager, ManipulatorManager
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Devices.DeviceFactory import DeviceManagerFactorySerialAbstract
from bin.Settings.SettingsEntity import SettingsEntity


class ManipulatorManagerFactory(DeviceManagerFactorySerialAbstract):
    def __init__(self, base_component, settings_entity=SettingsEntity("")):
        assert isinstance(settings_entity, SettingsSerialEntity)
        super(ManipulatorManagerFactory, self).__init__(settings_entity)
        self.base_component = base_component

    def create(self, *args, **kwargs):
        if self.port_exists():
            return ManipulatorManager(self.settings_entity).register(self.base_component)
        else:
            return NullManipulatorManager(self.settings_entity).register(self.base_component)
