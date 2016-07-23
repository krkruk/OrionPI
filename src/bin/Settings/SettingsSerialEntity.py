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
