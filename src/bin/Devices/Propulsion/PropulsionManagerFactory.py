from bin.Devices.DeviceFactory import DeviceFactorySerialAbstract
from bin.Devices.Propulsion import PropulsionManager, NullPropulsionManager
from bin.Settings.SettingsEntity import SettingsEntity
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity


class PropulsionManagerFactory(DeviceFactorySerialAbstract):
    def __init__(self, base_component, settings_entity=SettingsEntity("")):
        assert isinstance(settings_entity, SettingsSerialEntity)
        super(PropulsionManagerFactory, self).__init__(settings_entity)
        self.base_component = base_component

    def create(self, *args, **kwargs):
        if self.port_exists():
            return PropulsionManager(self.settings_entity).register(self.base_component)
        else:
            return NullPropulsionManager(self.settings_entity).register(self.base_component)
