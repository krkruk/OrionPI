from bin.Devices import EventlessDeviceManager, NullDeviceManager
from bin.Settings.SettingsEntity import SettingsEntity
from bin.IO.SerialEntity import SerialEntity
from circuits import BaseComponent, handler


class EventlessContainersManager(EventlessDeviceManager):
    def __init__(self, serial_sett_entity=SettingsEntity("")):
        EventlessDeviceManager.__init__(self, serial_sett_entity)

    def on_read_line(self, *args, **kwargs):
        pass


class ContainersManager(BaseComponent, EventlessContainersManager):
    def __init__(self, serial_sett_entity=SettingsEntity("")):
        BaseComponent.__init__(self)
        EventlessContainersManager.__init__(self, serial_sett_entity)
        self.device = SerialEntity(**self.device_conn).register(self)

    @handler("line_read", channel="containers")
    def on_read_line(self, *args, **kwargs):
        pass

    def write_line(self, line, *args, **kwargs):
        self.line_sent = line
        self.device.write_line(self.line_sent)
        

class NullContainersManager(BaseComponent, NullDeviceManager):
    def __init__(self, serial_sett_entity=SettingsEntity("")):
        BaseComponent.__init__(self)
        NullDeviceManager.__init__(self, serial_sett_entity)
