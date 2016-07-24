from bin.Dispatcher.IO.SerialEntity import SerialEntity
from bin.Dispatcher.Devices import DeviceAbstract
from circuits import BaseComponent
from circuits import handler
import json


class Propulsion(DeviceAbstract.Device):
    def __init__(self, device_manager):
        super(Propulsion, self).__init__(device_manager)


class EventlessPropulsionManager(DeviceAbstract.EventlessDeviceManager):
    def __init__(self, serial_conn={}):
        super(EventlessPropulsionManager, self).__init__(serial_conn)

    def on_read_line(self, *args, **kwargs):
        pass


class PropulsionManager(BaseComponent, DeviceAbstract.EventlessDeviceManager):
    def __init__(self, serial_conn={}):
        BaseComponent.__init__(self)
        DeviceAbstract.EventlessDeviceManager.__init__(self, serial_conn)
        self.device = SerialEntity(**serial_conn).register(self)

    @handler("line_read", channel="propulsion")
    def on_read_line(self, *args, **kwargs):
        pass

    def write_line(self, line, *args, **kwargs):
        self.line_sent = line
        self.device.write_line(self.line_sent)


class NullPropulsionManager(BaseComponent, DeviceAbstract.NullDeviceManager):
    def __init__(self, serial_conn={}):
        BaseComponent.__init__(self)
        DeviceAbstract.NullDeviceManager.__init__(self, serial_conn)
