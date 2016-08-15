from bin.Settings import SettingsManager, SettingsUDPEntity, SettingsSerialEntity, SettingsLoader, SettingsUpdaterTCPServer
from bin.Updater.UpdaterTCPServer import UpdaterTCPServer, update_acquired
from bin.Dispatcher.Devices.DeviceWholesale import DeviceWholesale
from bin.Dispatcher.DataController import DispatchController
from bin.Updater.Updater import UpdaterZIP, Updater
from bin.Dispatcher.Dictionary import SettingsKeys
import bin.Dispatcher.UDPReceiver as UDPReceiver
from circuits import BaseComponent, Debugger
from circuits import handler


class Main(BaseComponent):
    def __init__(self):
        super(Main, self).__init__()
        self.propulsion_settings = SettingsSerialEntity(SettingsKeys.PROPULSION)
        self.manipulator_settings = SettingsSerialEntity(SettingsKeys.MANIPULATOR)
        self.udp_settings = SettingsUDPEntity(SettingsKeys.UDP)
        self.tcp_updater_settings = SettingsUpdaterTCPServer(SettingsKeys.TCP_UPDATER)
        self.settings_entities = [self.propulsion_settings, self.manipulator_settings,
                                  self.udp_settings, self.tcp_updater_settings]

        self.settings_manager = SettingsManager("settings.json")
        self.settings_manager.add_entity(self.settings_entities)
        self.settings_manager.load()

        device_wholesaler = DeviceWholesale(self, [self.propulsion_settings, self.manipulator_settings])

        self.controller = DispatchController(device_wholesaler.sell_all())
        self.server = UDPReceiver.UDPReceiver(controller=self.controller,
                                              udp_sett_entity=self.udp_settings).register(self)

        self.tcp_updater = UpdaterTCPServer(self.tcp_updater_settings).register(self)

    @handler("update_acquired")
    def on_update_acquired(self):
        zip_alg = UpdaterZIP("update.zip")
        updater = Updater(zip_alg)
        if updater.update():
            updater.clear_update_file()
            updater.restart_all()


if __name__ == "__main__":
    (Main() + Debugger()).run()
