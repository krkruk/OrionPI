import bin.Dispatcher.Dictionary as Dict
import json


class Controller:
    def __init__(self):
        self.recent_line_acquired = ""

    def acquire_new_data(self, *args, **kwargs):
        try:
            line = args[0]
        except IndexError:
            return

        self.recent_line_acquired = line
        self._parse_json()
        self.handle_propulsion()
        self.handle_manipulator()
        self.handle_peripheries()

    def handle_propulsion(self):
        raise NotImplemented()

    def handle_manipulator(self):
        raise NotImplemented()

    def handle_peripheries(self):
        raise NotImplemented()

    def _parse_json(self):
        raise NotImplemented()


class DataController(Controller):
    def __init__(self, propulsion, manipulator, peripheries):
        super(DataController, self).__init__()
        self.curr_dict_data = None
        self.propulsion = propulsion
        self.manipulator = manipulator
        self.peripheries = peripheries

    def _parse_json(self):
        self.curr_dict_data = json.loads(self.recent_line_acquired)

    def handle_propulsion(self):
        propulsion_data = self.curr_dict_data.get(Dict.DeviceClass.PROPULSION, None)
        if propulsion_data:
            self.propulsion.update_data(propulsion_data)

    def handle_manipulator(self):
        manipulator_data = self.curr_dict_data.get(Dict.DeviceClass.MANIPULATOR, None)
        if manipulator_data:
            self.manipulator.update_data(manipulator_data)

    def handle_peripheries(self):
        peripheries_data = self.curr_dict_data.get(Dict.DeviceClass.PERIPHERIES, None)
        if peripheries_data:
            self.peripheries.update_data(peripheries_data)
