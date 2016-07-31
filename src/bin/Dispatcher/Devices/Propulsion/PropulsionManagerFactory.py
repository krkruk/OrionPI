from bin.Dispatcher.Devices.DeviceFactory import DeviceFactorySerialAbstract
from bin.Settings.SettingsEntity import SettingsEntity
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Dispatcher.utility.ServiceDiscoverer import get_port_name
from bin.Dispatcher.Devices.Propulsion.PropulsionManager import PropulsionManager, Propulsion, NullPropulsionManager


class PropulsionManagerFactory(DeviceFactorySerialAbstract):
    def __init__(self, base_component, settings_entity=SettingsEntity("")):
        super(PropulsionManagerFactory, self).__init__(settings_entity)
        self.base_component = base_component
        self.port = settings_entity.get_entry(SettingsSerialEntity.PORT) \
            if isinstance(settings_entity, SettingsSerialEntity) \
            else None

    def create(self):
        if self.port_exists():
            return PropulsionManager(self.settings_entity).register(self.base_component)
        else:
            return NullPropulsionManager(self.settings_entity).register(self.base_component)

    def port_exists(self):
        return get_port_name(self.port)

    def get_name(self):
        return "Factory of {} @port: {}".format(
            self.__class__.__name__, self.port_exists())