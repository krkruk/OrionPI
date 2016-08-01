from bin.Dispatcher.Devices.DeviceFactory import DeviceFactory
from bin.Dispatcher.Devices.Propulsion.PropulsionManagerFactory import PropulsionManagerFactory
from bin.Dispatcher.Devices.Propulsion.PropulsionManager import Propulsion


class PropulsionFactory(DeviceFactory):
    def __init__(self, manager_factory):
        DeviceFactory.__init__(self, manager_factory)

    def create(self, *args, **kwargs):
        propulsion_manager = self.device_manager_factory.create()
        return Propulsion(device_manager=propulsion_manager)

    def get_manager_factory_type(self):
        return PropulsionManagerFactory
