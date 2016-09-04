from tests.Dispatcher.DataCreator import CreateDeviceData
import json
import unittest
from bin.Devices.Containers.ContainersDevice import ContainersDevice
from bin.Devices.Containers.ContainersManager import EventlessContainersManager, NullContainersManager, \
    ContainersManager
from bin.Devices.Containers.ContainersFactory import ContainersFactory
from bin.Devices.Containers.ContainersManagerFactory import ContainersManagerFactory
from circuits import BaseComponent
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Dispatcher.Dictionary import SettingsKeys
from unittest.mock import MagicMock


class TestContainerDeviceDataFlow(unittest.TestCase):
    def setUp(self):
        self.eventless_mgr = EventlessContainersManager()
        self.null_mgr = NullContainersManager()
        self.sample_data = {"sample": "data"}
        self.data = CreateDeviceData()
        self.base_component = BaseComponent()

    def test_eventless_data_flow(self):
        container = ContainersDevice(self.eventless_mgr)
        container.update_data_incoming(self.sample_data)
        self.assertDictEqual(self.sample_data, json.loads(self.eventless_mgr.line_sent))

    def test_creation_of_containers_device_by_containers_factory(self):
        containers_settings = self._create_settings()
        containers_factory = ContainersFactory(ContainersManagerFactory(self.base_component, containers_settings))
        containers = containers_factory.create()
        self.assertIsInstance(containers, ContainersDevice)

    def test_creation_of_null_containers_manager(self):
        containers_manager_factory = ContainersManagerFactory(self.base_component, self._create_settings())
        containers_manager = containers_manager_factory.create()
        self.assertIsInstance(containers_manager, NullContainersManager)

    def test_creation_of_real_containers_manager(self):
        containers_manager_factory = ContainersManagerFactory(self.base_component, self._create_settings())
        containers_manager_factory.port_exists = MagicMock(return_value=containers_manager_factory.port)
        containers_manager = containers_manager_factory.create()
        self.assertIsInstance(containers_manager, ContainersManager)

    def _create_settings(self):
        containers_settings = SettingsSerialEntity(key=SettingsKeys.CONTAINERS)
        containers_settings.add_entries(self.data.containers_dict)
        return  containers_settings


if __name__ == "__main__":
    unittest.main()
