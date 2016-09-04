import json
import unittest
from unittest.mock import MagicMock
from bin.Devices.DeviceAbstract import Device
from bin.Devices.DeviceObserver import DeviceObserverInterface
from bin.Devices import NullDeviceManager


class MockObserver(DeviceObserverInterface):
    def __init__(self):
        self.data = ""

    def update(self, *args, **kwargs):
        self.data = args[0]


class TestDeviceAbstractObserverPattern(unittest.TestCase):
    def setUp(self):
        self.dev_id = "DEV"
        self.text_test_data = "test"
        self.test_content = {
                "Test1": 1,
                "Test2": 2
            }
        self.test_content_ascii = bytes(json.dumps(self.test_content), encoding="utf-8")
        self.test_json_dict = {
            self.dev_id: self.test_content
        }
        self.test_json = json.dumps(self.test_json_dict)
        self.test_json_ascii = bytes(self.test_json, encoding="utf-8")
        self.error_json = b'{"json":1, "json2"}'
        self.device = Device(self.dev_id, NullDeviceManager())

    def test_observer_notification(self):
        observers = [MockObserver() for _ in range(2)]
        self.device.add_observer(observers)
        self.device.notify_all(self.text_test_data)
        for observer in observers:
            self.assertEqual(observer.data, self.text_test_data)

    def test_parse_json(self):

        self.assertFalse(self.device._parse_to_json(self.error_json))

    def test_insert_id_into_data(self):
        inserted_data = self.device._insert_id_into_data(self.test_content)
        self.assertDictEqual(inserted_data, self.test_json_dict)

    def test_handle_data_outcoming(self):
        outcoming_data = self.device.handle_data_outcoming(self.test_content)
        self.assertDictEqual(outcoming_data, self.test_json_dict)

    def test_update_data_outcoming_correct_json(self):
        observer = MockObserver()
        self.device.add_observer(observer)
        self.device.notify_all = MagicMock()
        self.device.update_data_outcoming(self.test_content_ascii)
        self.assertTrue(self.device.notify_all.called)

    def test_update_outcoming_error_json(self):
        self.device.add_observer(MockObserver())
        self.device.notify_all = MagicMock()
        self.device.update_data_outcoming(self.error_json)
        self.assertFalse(self.device.notify_all.called)


if __name__ == "__main__":
    unittest.main()
