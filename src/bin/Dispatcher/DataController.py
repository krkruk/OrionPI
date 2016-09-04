import bin.Dispatcher.Dictionary as Dict
import json


class ControllerInterface:
    def acquire_new_data(self, *args, **kwargs):
        raise NotImplemented()

    def _parse_json(self):
        raise NotImplemented()


class ControllerAbstract(ControllerInterface):
    def __init__(self):
        self.recent_line_acquired = ""
        self.has_parsed_json = False

    def acquire_new_data(self, *args, **kwargs):
        try:
            line = args[0]
        except IndexError:
            return

        self.recent_line_acquired = line
        self._parse_json()
        if self.has_parsed_json:
            self.handle_propulsion()
            self.handle_manipulator()
            self.handle_peripheries()

    def handle_propulsion(self):
        raise NotImplemented()

    def handle_manipulator(self):
        raise NotImplemented()

    def handle_peripheries(self):
        raise NotImplemented()


class DataController(ControllerAbstract):
    def __init__(self, propulsion, manipulator, peripheries):
        super(DataController, self).__init__()
        self.curr_dict_data = None
        self.propulsion = propulsion
        self.manipulator = manipulator
        self.peripheries = peripheries

    def _parse_json(self):
        try:
            self.curr_dict_data = json.loads(self.recent_line_acquired)
            self.has_parsed_json = True
        except json.JSONDecodeError:
            self.has_parsed_json = False

    def handle_propulsion(self):
        propulsion_data = self.curr_dict_data.get(Dict.DeviceClass.PROPULSION, None)
        if propulsion_data:
            self.propulsion.update_data_incoming(propulsion_data)

    def handle_manipulator(self):
        manipulator_data = self.curr_dict_data.get(Dict.DeviceClass.MANIPULATOR, None)
        if manipulator_data:
            self.manipulator.update_data_incoming(manipulator_data)

    def handle_peripheries(self):
        peripheries_data = self.curr_dict_data.get(Dict.DeviceClass.CONTAINERS, None)
        if peripheries_data:
            self.peripheries.update_data_incoming(peripheries_data)


class DispatchController(ControllerInterface):
    def __init__(self, devices):
        assert isinstance(devices, list)
        self.devices = devices
        self.recent_line_acquired = ""
        self.has_parsed_json = False
        self.curr_dict_data = {}
        self.curr_dict_keys = []
        self.can_update = False

    def acquire_new_data(self, *args, **kwargs):
        try:
            line = args[0]
        except IndexError:
            return

        self.recent_line_acquired = line
        self._parse_json()
        if self.has_parsed_json:
            self._handle_devices()

    def _parse_json(self):
        try:
            self.curr_dict_data = json.loads(self.recent_line_acquired)
            self.has_parsed_json = True
        except json.JSONDecodeError:
            self.has_parsed_json = False

    def _handle_devices(self):
        self.curr_dict_keys = self.curr_dict_data.keys()
        for device in self.devices:
            device_id = device.get_id()
            self._verify_device_existence(device_id)
            self._update_device(device, device_id)

    def _verify_device_existence(self, device_id):
        if device_id in self.curr_dict_keys:
            self.can_update = True

    def _update_device(self, device, device_id):
        curr_data = self.curr_dict_data.get(device_id)
        if curr_data and self.can_update:
            device.update_data_incoming(curr_data)
        self.can_update = False
