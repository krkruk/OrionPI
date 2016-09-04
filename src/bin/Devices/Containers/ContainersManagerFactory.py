from bin.Devices.DeviceFactory import DeviceManagerFactorySerialAbstract
from bin.Devices.Containers import ContainersManager, NullContainersManager
from bin.Settings.SettingsEntity import SettingsEntity
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity


class ContainersManagerFactory(DeviceManagerFactorySerialAbstract):
    def __init__(self, base_component, settings_entity=SettingsEntity("")):
        assert isinstance(settings_entity, SettingsSerialEntity)
        DeviceManagerFactorySerialAbstract.__init__(self, settings_entity)
        self.base_component = base_component

    def create(self, *args, **kwargs):
        if self.port_exists():
            return ContainersManager(self.settings_entity).register(self.base_component)
        else:
            return NullContainersManager(self.settings_entity).register(self.base_component)
