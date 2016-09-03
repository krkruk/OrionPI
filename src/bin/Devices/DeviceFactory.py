from bin.Settings.SettingsEntity import SettingsEntity
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Utility.SerialDiscoverer import get_port_name


class DeviceFactoryAbstract:
    def __init__(self, settings_entity=SettingsEntity("")):
        self.settings_entity = settings_entity

    def create(self, *args, **kwargs):
        raise NotImplemented()

    def get_settings_entity(self):
        return self.settings_entity


class DeviceFactorySerialAbstract(DeviceFactoryAbstract):
    def __init__(self, settings_entity=SettingsEntity("")):
        DeviceFactoryAbstract.__init__(self, settings_entity)
        self.port = settings_entity.get_entry(SettingsSerialEntity.PORT)

    def port_exists(self):
        port = get_port_name(self.port)
        self.settings_entity.add_entry(SettingsSerialEntity.PORT, port)
        return port

    def get_name(self):
        return "Factory of {} @port: {}".format(
            self.__class__.__name__, self.port_exists())


class DeviceFactory(DeviceFactoryAbstract):
    def __init__(self, manager_factory):
        assert isinstance(manager_factory, self.get_manager_factory_type())
        self.device_manager_factory = manager_factory
        DeviceFactoryAbstract.__init__(self, manager_factory.get_settings_entity())

    def get_manager_factory_type(self):
        raise NotImplemented("")
