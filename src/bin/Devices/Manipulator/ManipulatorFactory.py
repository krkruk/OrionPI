from bin.Devices.Manipulator import ManipulatorManagerFactory
from bin.Devices.DeviceFactory import DeviceFactory
from bin.Devices.Manipulator import Manipulator


class ManipulatorFactory(DeviceFactory):
    def __init__(self, manager_factory):
        DeviceFactory.__init__(self, manager_factory)

    def create(self, *args, **kwargs):
        manipulator_manager = self.device_manager_factory.create()
        return Manipulator(device_manager=manipulator_manager)

    def get_manager_factory_type(self):
        return ManipulatorManagerFactory
