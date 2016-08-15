from bin.Settings.SettingsEntity import SettingsServerEntity


class SettingsUDPEntity(SettingsServerEntity):
    IP = "IP"
    PORT = "port"
    CHANNEL = "channel"
    BIND = "bind"

    def __init__(self, key):
        SettingsServerEntity.__init__(self,
                                      key,
                                      "127.0.0.1",
                                      5000,
                                      "UDPServer")
