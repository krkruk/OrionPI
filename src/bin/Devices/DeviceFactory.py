from bin.Settings.SettingsEntity import SettingsEntity


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

    def port_exists(self):
        raise NotImplemented()

    def get_name(self):
        raise NotImplemented()


class DeviceFactory(DeviceFactoryAbstract):
    def __init__(self, manager_factory):
        assert isinstance(manager_factory, self.get_manager_factory_type())
        self.device_manager_factory = manager_factory
        DeviceFactoryAbstract.__init__(self, manager_factory.get_settings_entity())

    def get_manager_factory_type(self):
        raise NotImplemented("")
