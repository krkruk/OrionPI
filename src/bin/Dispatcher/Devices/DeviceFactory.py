from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import Manipulator, EventlessManipulatorManager, NullManipulatorManager
from bin.Dispatcher.Devices.Propulsion.PropulsionManager import Propulsion, EventlessPropulsionManager, NullPropulsionManager
from bin.Dispatcher.Dictionary import SettingsKeys


class DeviceFactoryAbstract:
    def __init__(self):
        pass

    def create(self, device_name):
        raise NotImplemented()


class DeviceFactory(DeviceFactoryAbstract):
    def __init__(self):
        DeviceFactoryAbstract.__init__(self)

    def create(self, device_name):
        if device_name == SettingsKeys.PROPULSION:
            return NullPropulsionManager()
        elif device_name == SettingsKeys.MANIPULATOR:
            return NullManipulatorManager()
        else:
            return None
