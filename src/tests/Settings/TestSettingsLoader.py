from bin.Settings.SettingsManager import SettingsLoader, SettingsManagerMock
from bin.Settings.SettingsEntity import get_settings_entity_from_list
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Settings.SettingsUDPEntity import SettingsUDPEntity
from bin.Dispatcher.Dictionary import *
import unittest
from unittest.mock import MagicMock
import json


class TestSettingsLoader(unittest.TestCase):
    def setUp(self):
        self.propulsion_settings = SettingsSerialEntity(SettingsKeys.PROPULSION)
        self.manipulator_settings = SettingsSerialEntity(SettingsKeys.MANIPULATOR)
        self.udp_settings = SettingsUDPEntity(SettingsKeys.UDP)
        self.settings_list = [self.propulsion_settings,
                              self.manipulator_settings, self.udp_settings]

        self.mock_settings_manager = SettingsManagerMock("test_settings.json", self.settings_list)
        self.mock_settings_manager.save()
        self.mock_settings_manager.load()
        self.json_str_test = self.mock_settings_manager.json_string
        self.json_dict_test = json.loads(self.json_str_test)

        self.loader_params = {
            SettingsKeys.PROPULSION: SettingsSerialEntity,
            SettingsKeys.MANIPULATOR: SettingsSerialEntity,
            SettingsKeys.UDP: SettingsUDPEntity,
            SettingsKeys.PERIPHERIES: SettingsSerialEntity
        }
        self.loader = SettingsLoader("test_settings.json", self.loader_params)
        self.loader._file_exists = MagicMock(return_value=True)
        self.loader._open_file_get_json_dict = MagicMock(return_value=self.json_dict_test)

    def test_mock_file_exists(self):
        self.assertTrue(self.loader._file_exists())

    def test_mock_open_file_get_json_dict(self):
        self.assertDictEqual(self.json_dict_test, self.loader._open_file_get_json_dict())

    def test_load_function_whether_it_loaded_mock_json(self):
        self.loader.load()
        self.assertDictEqual(self.json_dict_test, self.loader.json_dict_data)

    def test_splitting_abilities_into_json(self):
        self.assertCountEqual(self.settings_list, self.loader.load())

    def test_compare_settings_serial_entity_to_serial_settings_entity_from_setup(self):
        propulsion = SettingsSerialEntity(SettingsKeys.PROPULSION)
        self.assertFalse(propulsion == self.propulsion_settings)

    def test_load_real_file_and_compare_with_default_settings(self):
        settings_loader = SettingsLoader("test_settings.json", self.loader_params)
        settings_devices = settings_loader.load()
        for device in settings_devices:
            init_device = get_settings_entity_from_list(self.settings_list, device.key)
            self.assertEqual(init_device, device)

    def print_load_parsing(self, load):
        print("settings", self.settings_list)
        print("loader", load.load())
        for settings, loader in zip(self.settings_list, load.load()):
            print("Assert:", settings == loader)
            print("Keys: {} - {}".format(settings.key, loader.key))
            print("Settings: {} - {}".format(settings.settings, loader.settings))
            print("DefaultSettings: {} - {}".format(settings.default_settings, loader.default_settings))
            print("===============\n")


if __name__ == "__main__":
    unittest.main()
