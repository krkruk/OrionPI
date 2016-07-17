from src.bin.Dispatcher.IO.IO import IOStream


class DeviceAbstract:
    def handle_data(self, data={}):
        raise NotImplemented()


class NullDevice(DeviceAbstract):
    def handle_data(self, data={}):
        pass


class Device(DeviceAbstract):
    def __init__(self, device_manager):
        self.data = {}
        self.device_manager = device_manager

    def handle_data(self, data={}):
        self.data = data


class EventlessDeviceManager(IOStream):
    def __init__(self, serial_conn={}):
        pass

    def on_read_line(self, *args, **kwargs):
        """Inform View class"""
        raise NotImplemented()

    def write_line(self, line, *args, **kwargs):
        """Write a line into the device"""
        raise NotImplemented()


class NullDeviceManager(EventlessDeviceManager):
    def __init__(self, serial_conn={}):
        super(NullDeviceManager, self).__init__(serial_conn)

    def on_read_line(self, *args, **kwargs):
        pass

    def write_line(self, line, *args, **kwargs):
        pass
