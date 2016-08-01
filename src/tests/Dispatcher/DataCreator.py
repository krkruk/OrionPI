from bin.Dispatcher.Dictionary import SettingsKeys
from bin.Settings.SettingsSerialEntity import SettingsSerialEntity
from bin.Settings.SettingsUDPEntity import SettingsUDPEntity


def add_to_dict(d, key, entry):
    d[key] = entry


class CreateDeviceData:
    def __init__(self):
        self.propulsion_key = SettingsKeys.PROPULSION
        self.manipulator_key = SettingsKeys.MANIPULATOR
        self.udp_key = SettingsKeys.UDP

        # key, data
        self.propulsion_serial_port = (SettingsSerialEntity.PORT, "/dev/ttyUSB0")
        self.propulsion_serial_baudrate = (SettingsSerialEntity.BAUDRATE, 115200)
        self.propulsion_serial_channel = (SettingsSerialEntity.CHANNEL, "propulsion")

        self.manipulator_serial_port = (SettingsSerialEntity.PORT, "/dev/ttyACM0")
        self.manipulator_serial_baudrate = (SettingsSerialEntity.BAUDRATE, 115200)
        self.manipulator_serial_channel = (SettingsSerialEntity.CHANNEL, "manipulator")

        self.udp_server_ip = (SettingsUDPEntity.IP, "127.0.0.1")
        self.udp_server_port = (SettingsUDPEntity.PORT, 5000)
        self.udp_server_channel = (SettingsUDPEntity.CHANNEL, "UDPServer")

        # compare
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

    def create_propulsion_settings_entity(self):
        propulsion = SettingsSerialEntity(key=self.propulsion_key)
        propulsion.add_entries(self.propulsion_dict)
        return propulsion

    def create_manipulator_settings_entity(self):
        manipulator = SettingsSerialEntity(key=self.manipulator_key)
        manipulator.add_entries(self.manipulator_dict)
        return manipulator

    def create_udp_server_settings_entity(self):
        udp_server = SettingsUDPEntity(key=self.udp_key)
        udp_server.add_entries(self.udp_dict)
        return udp_server
