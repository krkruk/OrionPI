from bin.Devices.Containers.ContainersManagerFactory import ContainersManagerFactory
from bin.Devices.DeviceFactory import DeviceFactory
from bin.Devices.Containers.ContainersDevice import ContainersDevice


class ContainersFactory(DeviceFactory):
    def __init__(self, manager_factory):
        DeviceFactory.__init__(self, manager_factory)

    def create(self, *args, **kwargs):
        containers_manager = self.device_manager_factory.create()
        return ContainersDevice(containers_manager)

    def get_manager_factory_type(self):
        return ContainersManagerFactory
