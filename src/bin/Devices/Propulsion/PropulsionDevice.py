from bin.Dispatcher.Dictionary import DeviceClass
from bin.Devices import Device


class Propulsion(Device):
    def __init__(self, device_manager):
        super(Propulsion, self).__init__(DeviceClass.PROPULSION, device_manager)
