from bin.Settings.SettingsEntity import SettingsEntity


class DeviceFactoryAbstract:
    def __init__(self, settings_entity=SettingsEntity("")):
        self.settings_entity = settings_entity

    def create(self):
        raise NotImplemented()

    def get_name(self):
        raise NotImplemented()


class DeviceFactorySerialAbstract(DeviceFactoryAbstract):
    def __init__(self, settings_entity=SettingsEntity("")):
        DeviceFactoryAbstract.__init__(self, settings_entity)

    def port_exists(self):
        raise NotImplemented()
