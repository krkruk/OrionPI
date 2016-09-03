from bin.Devices.DeviceFactory import DeviceFactorySerialAbstract
from bin.Devices.Containers.ContainersDevice import ContainersDevice, NullContainersDevice
from bin.Settings.SettingsEntity import SettingsEntity
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Utility.SerialDiscoverer import get_port_name


class ContainersManagerFactory(DeviceFactorySerialAbstract):
    def __init__(self, base_component, settings_entity=SettingsEntity("")):
        assert isinstance(settings_entity, SettingsSerialEntity)
        DeviceFactorySerialAbstract.__init__(self, settings_entity)
        self.base_component = base_component

    def create(self, *args, **kwargs):
        if self.port_exists():
            return ContainersDevice(self.settings_entity).register(self.base_component)
        else:
            return NullContainersDevice(self.settings_entity).register(self.base_component)
