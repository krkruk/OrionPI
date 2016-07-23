from bin.Dispatcher.Dictionary import *
from bin.Settings import *
import unittest


def add_to_dict(d, key, entry):
    d[key] = entry


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.propulsion_key = SettingsKeys.PROPULSION
        self.manipulator_key = SettingsKeys.MANIPULATOR
        self.udp_key = SettingsKeys.UDP

        #key, data
        self.propulsion_serial_port = (SettingsSerialEntity.PORT, "/dev/ttyUSB0")
        self.propulsion_serial_baudrate = (SettingsSerialEntity.BAUDRATE, 115200)
        self.propulsion_serial_channel = (SettingsSerialEntity.CHANNEL, "propulsion")

        self.manipulator_serial_port = (SettingsSerialEntity.PORT, "/dev/ttyACM0")
        self.manipulator_serial_baudrate = (SettingsSerialEntity.BAUDRATE, 115200)
        self.manipulator_serial_channel = (SettingsSerialEntity.CHANNEL, "manipulator")

        self.udp_server_ip = (SettingsUDPEntity.IP, "127.0.0.1")
        self.udp_server_port = (SettingsUDPEntity.PORT, 5000)
        self.udp_server_channel = (SettingsUDPEntity.CHANNEL, "UDPServer")

        #compare
        self.propulsion_dict = {}
        add_to_dict(self.propulsion_dict, *self.propulsion_serial_port)
        add_to_dict(self.propulsion_dict, *self.propulsion_serial_baudrate)
        add_to_dict(self.propulsion_dict, *self.propulsion_serial_channel)

        self.manipulator_dict = {}
        add_to_dict(self.manipulator_dict, *self.manipulator_serial_port)
        add_to_dict(self.manipulator_dict, *self.manipulator_serial_baudrate)
        add_to_dict(self.manipulator_dict, *self.manipulator_serial_channel)

        self.udp_dict = {}
        add_to_dict(self.udp_dict, *self.udp_server_ip)
        add_to_dict(self.udp_dict, *self.udp_server_port)
        add_to_dict(self.udp_dict, *self.udp_server_channel)

    def test_create_propulsion_entity_and_check_correctness(self):
        propulsion_entity = SettingsSerialEntity(key=self.propulsion_key)
        propulsion_entity.add_entry(*self.propulsion_serial_port)
        propulsion_entity.add_entry(*self.propulsion_serial_baudrate)
        propulsion_entity.add_entry(*self.propulsion_serial_channel)
        self.assertDictEqual(self.propulsion_dict, propulsion_entity.settings)

    def test_create_manipulator_entity_and_check_correctness(self):
        manipulator_entity = SettingsSerialEntity(key=self.manipulator_key)
        manipulator_entity.add_entry(*self.manipulator_serial_port)
        manipulator_entity.add_entry(*self.manipulator_serial_baudrate)
        manipulator_entity.add_entry(*self.manipulator_serial_channel)
        self.assertDictEqual(self.manipulator_dict, manipulator_entity.settings)

    def test_create_udp_entity_and_check_correctness(self):
        udp_entity = SettingsUDPEntity(key=self.udp_key)
        udp_entity.add_entry(*self.udp_server_ip)
        udp_entity.add_entry(*self.udp_server_port)
        udp_entity.add_entry(*self.udp_server_channel)
        self.assertDictEqual(self.udp_dict, udp_entity.settings)

    def test_create_propulsion_entries_and_check_correctness(self):
        propulsion_entity = SettingsSerialEntity(key=self.propulsion_key)
        propulsion_entity.add_entries(self.propulsion_dict)
        self.assertDictEqual(self.propulsion_dict, propulsion_entity.settings)

    def test_get_serial_existing_entry(self):
        propulsion_entity = SettingsSerialEntity(key=self.propulsion_key)
        propulsion_entity.add_entry(*self.propulsion_serial_port)
        self.assertEqual(self.propulsion_dict[SettingsSerialEntity.PORT],
                         propulsion_entity.get_entry(SettingsSerialEntity.PORT))

    def test_get_serial_non_existing_entry_expect_return_default(self):
        propulsion_entity = SettingsSerialEntity(key=self.propulsion_key)
        propulsion_entity.add_entry(*self.propulsion_serial_port)
        self.assertTrue(propulsion_entity.get_entry(SettingsSerialEntity.CHANNEL))

    def test_get_serial_non_existing_port(self):
        propulsion_entity = SettingsSerialEntity(key=self.propulsion_key)
        self.assertFalse(propulsion_entity.get_entry(SettingsSerialEntity.PORT))

    def test_get_udp_existing_entry(self):
        udp_entity = SettingsUDPEntity(key=self.udp_key)
        udp_entity.add_entry(*self.udp_server_ip)
        self.assertEqual(self.udp_dict[SettingsUDPEntity.IP],
                         udp_entity.get_entry(SettingsUDPEntity.IP))

    def test_get_udp_non_existing_entry(self):
        udp_entity = SettingsUDPEntity(key=self.udp_key)
        self.assertTrue(udp_entity.get_entry(SettingsUDPEntity.IP))

    def test_getting_dict_if_all_elements_entered(self):
        propulsion_entity = SettingsSerialEntity(key=self.propulsion_key)
        propulsion_entity.add_entries(self.propulsion_dict)
        self.assertDictEqual(self.propulsion_dict, propulsion_entity.get_settings())

    def test_getting_dict_if_no_value_entered_expect_default(self):
        propulsion_entity = SettingsSerialEntity(key=self.propulsion_key)
        self.assertTrue(propulsion_entity.get_settings())


if __name__ == "__main__":
    unittest.main()


