from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import Manipulator, ManipulatorManager, NullManipulatorManager
from bin.Dispatcher.Devices.Propulsion.PropulsionManager import Propulsion, PropulsionManager, NullPropulsionManager
from bin.Dispatcher.Devices.Manipulator.ManipulatorManagerFactory import ManipulatorManagerFactory
from bin.Dispatcher.Devices.Propulsion.PropulsionManagerFactory import PropulsionManagerFactory
from bin.Dispatcher.Devices.Manipulator.ManipulatorFactory import ManipulatorFactory
from bin.Dispatcher.Devices.Propulsion.PropulsionFactory import PropulsionFactory
from bin.Settings import SettingsManager, SettingsUDPEntity, SettingsSerialEntity
from bin.Dispatcher.Devices.DeviceAbstract import NullDevice
from bin.Dispatcher.DataController import DataController
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

        propulsion_manager_factory = PropulsionManagerFactory(self, self.propulsion_settings)
        manipulator_manager_factory = ManipulatorManagerFactory(self, self.manipulator_settings)

        self.propulsion = PropulsionFactory(propulsion_manager_factory).create()
        self.manipulator = ManipulatorFactory(manipulator_manager_factory).create()

        self.controller = DataController(self.propulsion, self.manipulator, NullDevice())
        self.server = UDPReceiver.UDPReceiver(controller=self.controller,
                                              udp_sett_entity=self.udp_settings).register(self)


if __name__ == "__main__":
    (Main() + Debugger()).run()
