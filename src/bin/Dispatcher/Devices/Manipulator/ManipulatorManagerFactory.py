from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import NullManipulatorManager, ManipulatorManager, Manipulator
from bin.Dispatcher.Devices.DeviceFactory import DeviceFactorySerialAbstract
from bin.Dispatcher.utility.ServiceDiscoverer import get_port_name
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Settings.SettingsEntity import SettingsEntity


class ManipulatorManagerFactory(DeviceFactorySerialAbstract):
    def __init__(self, base_component, settings_entity=SettingsEntity("")):
        assert isinstance(settings_entity, SettingsSerialEntity)
        super(ManipulatorManagerFactory, self).__init__(settings_entity)
        self.base_component = base_component
        self.port = settings_entity.get_entry(SettingsSerialEntity.PORT)

    def create(self, *args, **kwargs):
        if self.port_exists():
            return ManipulatorManager(self.settings_entity).register(self.base_component)
        else:
            return NullManipulatorManager(self.settings_entity).register(self.base_component)

    def port_exists(self):
        port = get_port_name(self.port)
        self.settings_entity.add_entry(SettingsSerialEntity.PORT, port)
        return port

    def get_name(self):
        return "Factory of {} @port: {}".format(
            self.__class__.__name__, self.port_exists())
