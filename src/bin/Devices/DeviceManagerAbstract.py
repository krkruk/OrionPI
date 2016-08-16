from bin.IO import IOStream
from bin.Settings import SettingsEntity


class EventlessDeviceManager(IOStream):
    def __init__(self, serial_sett_entity=SettingsEntity("")):
        self.is_line_sent = False
        self.line_sent = ""
        self.serial_sett_entity = serial_sett_entity
        self.device_conn = serial_sett_entity.get_settings()

    def write_line(self, line, *args, **kwargs):
        self.line_sent = line
        self.is_line_sent = True


class NullDeviceManager(EventlessDeviceManager):
    def __init__(self, serial_sett_entity=SettingsEntity("")):
        super(NullDeviceManager, self).__init__(serial_sett_entity)

    def on_read_line(self, *args, **kwargs):
        pass

    def write_line(self, line, *args, **kwargs):
        pass
