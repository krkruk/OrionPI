from src.bin.Dispatcher.Devices.Propulsion.PropulsionManager import *
from src.bin.Dispatcher.Devices.DeviceAbstract import *
from src.bin.Dispatcher.UDPReceiver import *
from src.bin.Dispatcher.Dictionary import *
import unittest
import json


simple_dict = {"a": 1, "b": 2, "c": "cccc"}
system_dict = {
    DeviceClass.PROPULSION: {
        PropulsionKeys.LEFT_WHEEL_SPEED: 100,
        PropulsionKeys.RIGHT_WHEEL_SPEED: 100
    },
    DeviceClass.MANIPULATOR: {
        ManipulatorKeysUC.TURRET: -20
    }
}


class TestController(unittest.TestCase):
    def setUp(self):
        self.address = ("127.0.0.1", 1234)
        self.simple_json = json.dumps(simple_dict)
        self.system_json = json.dumps(system_dict)
        self.propulsion_json = json.dumps(system_dict[DeviceClass.PROPULSION])
        self.manipulator_json = json.dumps(system_dict[DeviceClass.MANIPULATOR])

    def test_udpreceiver_to_data_controller_communication(self):
        controller = DataController(NullDevice(), NullDevice(), NullDevice())
        recvr = EventlessUDPReceiver(controller=controller)
        recvr.on_read_line(self.address, self.simple_json)
        self.assertEqual(self.simple_json, controller.recent_line_acquired)

    def test_data_handling_to_device(self):
        manager = EventlessPropulsionManager(serial_conn={})
        propulsion = Propulsion(device_manager=manager)
        controller = DataController(propulsion, NullDevice(), NullDevice())
        controller.acquire_new_data(self.system_json)
        self.assertTrue(manager.is_line_sent, "Line not sent")

    def test_expected_line_handling_propulsion(self):
        manager = EventlessPropulsionManager(serial_conn={})
        propulsion = Propulsion(device_manager=manager)
        controller = DataController(propulsion, NullDevice(), NullDevice())
        controller.acquire_new_data(self.system_json)
        self.assertEqual(self.propulsion_json, manager.line_sent)

    def test_expected_line_handling_manipulator(self):
        manager = EventlessPropulsionManager(serial_conn={})
        manipulator = Propulsion(device_manager=manager)
        controller = DataController(NullDevice(), manipulator, NullDevice())
        controller.acquire_new_data(self.system_json)
        self.assertEqual(self.manipulator_json, manager.line_sent)


if __name__ == "__main__":
    unittest.main()
