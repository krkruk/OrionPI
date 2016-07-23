from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import Manipulator, ManipulatorManager
from bin.Dispatcher.Devices.Propulsion.PropulsionManager import Propulsion, PropulsionManager
from bin.Settings import SettingsManager, SettingsUDPEntity, SettingsSerialEntity
from bin.Dispatcher.Dictionary import SettingsKeys
from bin.Dispatcher.Devices.DeviceAbstract import NullDevice
from bin.Dispatcher.DataController import DataController
import bin.Dispatcher.UDPReceiver as UDPReceiver
from circuits import BaseComponent, handler, Debugger

# udp_conn = {"bind": ("127.0.0.1", 3333), "channel": "UDPServer"}
# propulsion_conn = {"port": "/dev/ttyACM0", "channel": "propulsion"}
# manipulator_conn = {"port": "/dev/ttyACM1", "channel": "manipulator"}


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

        propulsion_conn = self.propulsion_settings.get_settings()
        manipulator_conn = self.manipulator_settings.get_settings()
        udp_conn = self.udp_settings.get_settings()

        self.propulsion_manager = PropulsionManager(propulsion_conn).register(self)
        self.manipulator_manager = ManipulatorManager(manipulator_conn).register(self)

        self.propulsion = Propulsion(device_manager=self.propulsion_manager)
        self.manipulator = Manipulator(device_manager=self.manipulator_manager)

        self.controller = DataController(self.propulsion, self.manipulator, NullDevice())
        self.server = UDPReceiver.UDPReceiver(controller=self.controller,
                                              udp_conn=udp_conn).register(self)


if __name__ == "__main__":
    (Main() + Debugger()).run()
