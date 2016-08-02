from bin.Settings.SettingsEntity import SettingsEntity


class SettingsSerialEntity(SettingsEntity):
    PORT = "port"
    BAUDRATE = "baudrate"
    CHANNEL = "channel"

    def __init__(self, key):
        SettingsEntity.__init__(self, key)
        self.default_settings = {
            self.PORT: "",
            self.BAUDRATE: 115200,
            self.CHANNEL: "serial"
        }

    def __eq__(self, other):
        if not isinstance(other, SettingsEntity):
            return False
        if (self.key == other.key and self.settings == other.settings and
                    self.default_settings == other.default_settings):
            return True
        else:
            return False
