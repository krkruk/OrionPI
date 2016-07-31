from bin.Dispatcher.Devices.DeviceFactory import DeviceFactorySerialAbstract
from bin.Settings.SettingsEntity import SettingsEntity
from bin.Dispatcher.utility.ServiceDiscoverer import get_port_name
from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import NullManipulatorManager, ManipulatorManager, Manipulator
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity


class ManipulatorManagerFactory(DeviceFactorySerialAbstract):
    def __init__(self, base_component, settings_entity=SettingsEntity("")):
        super(ManipulatorManagerFactory, self).__init__(settings_entity)
        self.base_component = base_component
        self.port = settings_entity.get_entry(SettingsSerialEntity.PORT) \
            if isinstance(settings_entity, SettingsSerialEntity) \
            else None

    def create(self):
        if self.port_exists():
            return ManipulatorManager(self.settings_entity).register(self.base_component)
        else:
            return NullManipulatorManager(self.settings_entity).register(self.base_component)

    def port_exists(self):
        return get_port_name(self.port)

    def get_name(self):
        return "Factory of {} @port: {}".format(
            self.__class__.__name__, self.port_exists())
