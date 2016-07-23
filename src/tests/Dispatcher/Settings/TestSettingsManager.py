import unittest
from bin.Settings import *
from bin.Dispatcher.Dictionary import *


def add_to_dict(d, key, entry):
    d[key] = entry


class TestSettingsManager(unittest.TestCase):
    def setUp(self):
        self.propulsion_key = SettingsKeys.PROPULSION
        self.udp_key = SettingsKeys.UDP

        # key, data
        self.propulsion_serial_port = (SettingsSerialEntity.PORT, "/dev/ttyUSB0")
        self.propulsion_serial_baudrate = (SettingsSerialEntity.BAUDRATE, 115200)
        self.propulsion_serial_channel = (SettingsSerialEntity.CHANNEL, "propulsion")

        self.udp_server_ip = (SettingsUDPEntity.IP, "127.0.0.1")
        self.udp_server_port = (SettingsUDPEntity.PORT, 5000)
        self.udp_server_channel = (SettingsUDPEntity.CHANNEL, "UDPServer")

        #compare
        self.propulsion_dict = {}
        add_to_dict(self.propulsion_dict, *self.propulsion_serial_port)
        add_to_dict(self.propulsion_dict, *self.propulsion_serial_baudrate)
        add_to_dict(self.propulsion_dict, *self.propulsion_serial_channel)

        self.udp_dict = {}
        add_to_dict(self.udp_dict, *self.udp_server_ip)
        add_to_dict(self.udp_dict, *self.udp_server_port)
        add_to_dict(self.udp_dict, *self.udp_server_channel)

        #serial and udp entities
        self.propulsion_entity = SettingsSerialEntity(key=self.propulsion_key)
        self.udp_entity = SettingsUDPEntity(key=self.udp_key)

    def test_load_default_settings(self):
        manager = SettingsManagerMock("settings.json")
        manager.add_entity(self.propulsion_entity)
        manager.load()
        data = self.propulsion_entity.get_settings_entity_dict()
        self.assertDictEqual(self.propulsion_entity.default_settings,
                             data[SettingsKeys.PROPULSION])

    def test_save_default_settings(self):
        manager = SettingsManagerMock("settings.json")
        manager.add_entity(self.propulsion_entity)
        manager.add_entity(self.udp_entity)
        manager.save()
        self.assertTrue(manager.json_string)

    def test_settings_manager(self):
        manager = SettingsManager("test_settings.json")
        manager.add_entity(self.propulsion_entity)
        manager.add_entity(self.udp_entity)
        manager.save()
        manager.load()
        self.assertTrue((self.udp_entity.get_settings_entity_dict() and
                        self.propulsion_entity.get_settings_entity_dict()))


if __name__ == "__main__":
    unittest.main()
