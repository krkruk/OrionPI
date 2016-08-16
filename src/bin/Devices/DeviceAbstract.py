import json


class DeviceAbstract:
    def __init__(self, device_id):
        self.id = device_id

    def update_data(self, data={}):
        raise NotImplemented()

    def handle_data(self, data={}):
        raise NotImplemented()


class NullDevice(DeviceAbstract):
    def __init__(self):
        DeviceAbstract.__init__(self, "NullDevice")

    def update_data(self, data={}):
        pass

    def handle_data(self, data={}):
        pass

    def __bool__(self):
        return False


class Device(DeviceAbstract):
    def __init__(self, device_id, device_manager):
        DeviceAbstract.__init__(self, device_id)
        self.data = {}
        self.line = ""
        self.device_manager = device_manager

    def update_data(self, data={}):
        self.data = self.handle_data(data)
        self.line = json.dumps(self.data, separators=(',', ':'))
        self.device_manager.write_line(self.line)

    def handle_data(self, data={}):
        """Influences the data that is _passed into the function.
        It allows modifying the structure of the data
        that is to be sent to the device.
        By default the function returns an unmodified
        value received from EventlessDeviceManager and its children."""
        return data

    def get_id(self):
        return self.id


