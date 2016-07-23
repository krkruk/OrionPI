from bin.Dispatcher.IO.SerialEntity import SerialEntity
from bin.Dispatcher.Devices import DeviceAbstract
import bin.Dispatcher.Devices.Manipulator.ManipulatorJSONTranslator as Translator
from circuits import BaseComponent
from circuits import handler
import json


class Manipulator(DeviceAbstract.Device):
    def __init__(self, device_manager):
        super(Manipulator, self).__init__(device_manager)
        self.translator = Translator.ManipulatorJSONTranslatorRPiToManipulator()

    def handle_data(self, data={}):
        d = self.translator.translate_to_uc(data)
        return d


class EventlessManipulatorManager(DeviceAbstract.EventlessDeviceManager):
    def __init__(self, serial_conn={}):
        super(EventlessManipulatorManager, self).__init__(serial_conn)

    def on_read_line(self, *args, **kwargs):
        pass


class ManipulatorManager(BaseComponent, EventlessManipulatorManager):
    def __init__(self, serial_conn={}):
        BaseComponent.__init__(self)
        EventlessManipulatorManager.__init__(self, serial_conn)
        self.device = SerialEntity(**serial_conn).register(self)

    @handler("line_read", channel="manipulator")
    def on_read_line(self, *args, **kwargs):
        pass

    def write_line(self, line, *args, **kwargs):
        self.line_sent = line
        self.device.write_line(self.line_sent)
