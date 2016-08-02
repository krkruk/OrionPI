from bin.Settings.SettingsEntity import SettingsEntity


class SettingsUDPEntity(SettingsEntity):
    IP = "IP"
    PORT = "port"
    CHANNEL = "channel"
    BIND = "bind"

    def __init__(self, key):
        SettingsEntity.__init__(self, key)
        self.default_settings = {
            self.IP: "127.0.0.1",
            self.PORT: 5000,
            self.CHANNEL: "UDPServer"
        }

    def get_settings(self):
        loaded_settings = SettingsEntity.get_settings(self)
        settings = {self.BIND: (loaded_settings[self.IP],
                                loaded_settings[self.PORT]),
                    self.CHANNEL: loaded_settings[self.CHANNEL]}
        return settings

    def __eq__(self, other):
        if not isinstance(other, SettingsEntity):
            return False
        if (self.key == other.key and self.settings == other.settings and
                    self.default_settings == other.default_settings):
            return True
        else:
            return False
