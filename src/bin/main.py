from bin.Settings import SettingsManager, SettingsUDPEntity, SettingsSerialEntity
from bin.Dispatcher.Devices.DeviceWholesale import DeviceWholesale
from bin.Dispatcher.DataController import DispatchController
from bin.Dispatcher.Dictionary import SettingsKeys
import bin.Dispatcher.UDPReceiver as UDPReceiver
from circuits import BaseComponent, Debugger


class Main(BaseComponent):
    def __init__(self):
        super(Main, self).__init__()
        self.propulsion_settings = SettingsSerialEntity(SettingsKeys.PROPULSION)
        self.manipulator_settings = SettingsSerialEntity(SettingsKeys.MANIPULATOR)
        self.udp_settings = SettingsUDPEntity(SettingsKeys.UDP)
        self.settings_entities = [self.propulsion_settings, self.manipulator_settings,
                                  self.udp_settings]

        self.settings_manager = SettingsManager("settings.json")
        self.settings_manager.add_entity(self.settings_entities)
        self.settings_manager.load()

        device_wholesaler = DeviceWholesale(self, [self.propulsion_settings, self.manipulator_settings])

        self.controller = DispatchController(device_wholesaler.sell_all())
        self.server = UDPReceiver.UDPReceiver(controller=self.controller,
                                              udp_sett_entity=self.udp_settings).register(self)


if __name__ == "__main__":
    (Main() + Debugger()).run()
