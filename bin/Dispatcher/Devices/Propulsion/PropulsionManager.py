from src.bin.Dispatcher.IO.SerialEntity import SerialEntity
from src.bin.Dispatcher.Devices import DeviceAbstract
from circuits import BaseComponent
from circuits import handler
import json


class Propulsion(DeviceAbstract.Device):
    def __init__(self, device_manager):
        super(Propulsion, self).__init__(device_manager)

    def handle_data(self, data={}):
        self.data = data
        self.device_manager.write_line(self.data)


class EventlessPropulsionManager(DeviceAbstract.EventlessDeviceManager):
    def __init__(self, serial_conn={}):
        super(EventlessPropulsionManager, self).__init__(serial_conn)
        self.is_line_sent = False
        self.line_sent = ""

    def on_read_line(self, *args, **kwargs):
        pass

    def write_line(self, line, *args, **kwargs):
        self.line_sent = json.dumps(line)
        self.is_line_sent = True


class PropulsionManager(BaseComponent, DeviceAbstract.EventlessDeviceManager):
    def __init__(self, serial_conn={}):
        BaseComponent.__init__(self)
        DeviceAbstract.EventlessDeviceManager.__init__(serial_conn)
        self.device = SerialEntity(**serial_conn).register(self)

    @handler("line_read", channel="propulsion")
    def on_read_line(self, *args, **kwargs):
        pass

    def write_line(self, line, *args, **kwargs):
        line = json.dumps(line)
        self.device.write_line(line)
