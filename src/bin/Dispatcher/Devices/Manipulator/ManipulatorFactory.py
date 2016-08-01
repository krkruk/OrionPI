from bin.Dispatcher.Devices.DeviceFactory import DeviceFactory
from bin.Dispatcher.Devices.Manipulator.ManipulatorManagerFactory import ManipulatorManagerFactory
from bin.Dispatcher.Devices.Manipulator.ManipulatorManager import Manipulator


class ManipulatorFactory(DeviceFactory):
    def __init__(self, manager_factory):
        DeviceFactory.__init__(self, manager_factory)

    def create(self, *args, **kwargs):
        manipulator_manager = self.device_manager_factory.create()
        return Manipulator(device_manager=manipulator_manager)

    def get_manager_factory_type(self):
        return ManipulatorManagerFactory
