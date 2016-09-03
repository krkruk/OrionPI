from bin.Dispatcher.Dictionary import DeviceClass
from bin.Devices import Device, NullDevice


class ContainersDevice(Device):
    def __init__(self, device_manager):
        Device.__init__(self, DeviceClass.CONTAINERS, device_manager)


class NullContainersDevice(NullDevice):
    def __init__(self, *args, **kwargs):
        NullDevice.__init__(self)