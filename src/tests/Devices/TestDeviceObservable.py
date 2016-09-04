import unittest
from bin.Devices.DeviceObservable import DeviceObservableAbstract


class TestDeviceObservable(unittest.TestCase):
    def setUp(self):
        self.single_data = "single_data"
        self.list_of_data = [i for i in range(10)]
        self.observable = DeviceObservableAbstract()

    def test_append_single_data(self):
        self.observable.add_observer(self.single_data)
        self.assertTrue(self.single_data in self.observable.observers)

    def test_append_list(self):
        self.observable.add_observer(self.list_of_data)
        self.assertTrue(len(self.observable.observers) > 1)


if __name__ == "__main__":
    unittest.main()
