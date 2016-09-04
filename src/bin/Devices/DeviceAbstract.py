from bin.Devices.DeviceObservable import DeviceObservableAbstract
import json


class DeviceInterface:
    def update_data_incoming(self, data={}):
        raise NotImplemented()

    def handle_data_incoming(self, data={}):
        raise NotImplemented()

    def update_data_outcoming(self, data=b""):
        raise NotImplemented()

    def handle_data_outcoming(self, data=b""):
        raise NotImplemented()


class DeviceAbstract(DeviceInterface):
    def __init__(self, device_id):
        self.id = device_id


class NullDevice(DeviceAbstract):
    def __init__(self):
        DeviceAbstract.__init__(self, "NullDevice")

    def update_data_incoming(self, data={}):
        pass

    def handle_data_incoming(self, data={}):
        pass

    def update_data_outcoming(self, data=b""):
        pass

    def handle_data_outcoming(self, data=b""):
        pass

    def __bool__(self):
        return False


class Device(DeviceAbstract, DeviceObservableAbstract):
    def __init__(self, device_id, device_manager):
        DeviceAbstract.__init__(self, device_id)
        DeviceObservableAbstract.__init__(self)
        self.data = {}
        self.line = ""
        self.device_manager = device_manager
        self.device_manager.set_device_model(self)

    def get_id(self):
        return self.id

    def update_data_incoming(self, data={}):
        self.data = self.handle_data_incoming(data)
        self.line = json.dumps(self.data, separators=(',', ':'))
        self.device_manager.write_line(self.line)

    def handle_data_incoming(self, data={}):
        """Influences the data that is _passed into the function.
        It allows modifying the structure of the data
        that is to be sent to the device.
        By default the function returns an unmodified
        value received from EventlessDeviceManager and its children."""
        return data

    def notify_all(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)

    def update_data_outcoming(self, data=b""):
        data = self._standarize_input_data(data)
        data_json = self._parse_to_json(data)
        if not data_json:
            return
        data_json = self.handle_data_outcoming(data_json)

        line_out = json.dumps(data_json, separators=(',', ':'))
        self.notify_all(line_out)

    def handle_data_outcoming(self, data={}):
        return self._insert_id_into_data(data)

    def _standarize_input_data(self, data):
        return data.decode() if isinstance(data, bytes) else data

    def _parse_to_json(self, data=b""):
        if isinstance(data, bytes) or isinstance(data, bytearray):
            data = data.decode()
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return None

    def _insert_id_into_data(self, data={}):
        return {self.get_id(): data}

    def __bool__(self):
        return True
