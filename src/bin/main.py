from bin.Settings.SettingsUpdaterTCPServer import SettingsUpdaterTCPServer
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Settings.SettingsUpdater import SettingsUpdaterEntity
from bin.Dispatcher.DataController import DispatchController
from bin.Settings.SettingsUDPEntity import SettingsUDPEntity
from bin.Updater.UpdaterTCPServer import UpdaterTCPServer
from bin.Settings.SettingsManager import SettingsManager
from bin.Devices.DeviceWholesale import DeviceWholesale
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
        self.containers_settings = SettingsSerialEntity(SettingsKeys.CONTAINERS)
        self.udp_settings = SettingsUDPEntity(SettingsKeys.UDP)
        self.tcp_updater_settings = SettingsUpdaterTCPServer(SettingsKeys.TCP_UPDATER_SERVER)
        self.updater_settings = SettingsUpdaterEntity(SettingsKeys.UPDATER)
        self.settings_entities = [self.propulsion_settings, self.manipulator_settings,
                                  self.udp_settings, self.tcp_updater_settings,
                                  self.updater_settings, self.containers_settings]

        self.settings_manager = SettingsManager("settings.json")
        self.settings_manager.add_entity(self.settings_entities)
        self.settings_manager.load()

        device_wholesaler = DeviceWholesale(self, [self.propulsion_settings,
                                                   self.manipulator_settings,
                                                   self.containers_settings])

        self.controller = DispatchController(device_wholesaler.sell_all())
        self.server = UDPReceiver.UDPReceiver(controller=self.controller,
                                              udp_sett_entity=self.udp_settings).register(self)

        self.tcp_updater = UpdaterTCPServer(self.tcp_updater_settings).register(self)

    @handler("update_acquired")
    def on_update_acquired(self):
        settings = self.updater_settings.get_settings()
        zip_alg = UpdaterZIP(**settings)
        updater = Updater(zip_alg)
        if updater.update():
            updater.clear_update_file()
            updater.restart_all()


if __name__ == "__main__":
    (Main() + Debugger()).run()
