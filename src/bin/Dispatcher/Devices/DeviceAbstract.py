from bin.Dispatcher.IO.IO import IOStream
import json


class DeviceAbstract:
    def update_data(self, data={}):
        raise NotImplemented()

    def handle_data(self, data={}):
        raise NotImplemented()


class NullDevice(DeviceAbstract):
    def update_data(self, data={}):
        pass

    def handle_data(self, data={}):
        pass


class Device(DeviceAbstract):
    def __init__(self, device_manager):
        self.data = {}
        self.line = ""
        self.device_manager = device_manager

    def update_data(self, data={}):
        self.data = self.handle_data(data)
        self.line = json.dumps(self.data)
        self.device_manager.write_line(self.line)

    def handle_data(self, data={}):
        """Influences the data that is passed into the function.
        It allows modifying the structure of the data
        that is to be sent to the device.
        By default the function returns an unmodified
        value received from EventlessDeviceManager and its children."""
        return data


class EventlessDeviceManager(IOStream):
    def __init__(self, serial_conn={}):
        self.is_line_sent = False
        self.line_sent = ""

    def on_read_line(self, *args, **kwargs):
        raise NotImplemented()

    def write_line(self, line, *args, **kwargs):
        self.line_sent = line
        self.is_line_sent = True


class NullDeviceManager(EventlessDeviceManager):
    def __init__(self, serial_conn={}):
        super(NullDeviceManager, self).__init__(serial_conn)

    def on_read_line(self, *args, **kwargs):
        pass

    def write_line(self, line, *args, **kwargs):
        pass
