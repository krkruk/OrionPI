from bin.IO import IOStream
from bin.Settings import SettingsEntity
from bin.Devices import NullDevice


class EventlessDeviceManager(IOStream):
    def __init__(self, serial_sett_entity=SettingsEntity(""), device_model=NullDevice()):
        self.is_line_sent = False
        self.line_sent = ""
        self.serial_sett_entity = serial_sett_entity
        self.device_conn = serial_sett_entity.get_settings()
        self.device_model = device_model

    def write_line(self, line, *args, **kwargs):
        self.line_sent = line
        self.is_line_sent = True

    def set_device_model(self, device_model):
        self.device_model = device_model


class NullDeviceManager(EventlessDeviceManager):
    def __init__(self, serial_sett_entity=SettingsEntity("")):
        super(NullDeviceManager, self).__init__(serial_sett_entity)

    def on_read_line(self, *args, **kwargs):
        pass

    def write_line(self, line, *args, **kwargs):
        pass
