from bin.Settings.SettingsEntity import SettingsServerEntity


class SettingsUpdaterTCPServer(SettingsServerEntity):
    def __init__(self, key):
        SettingsServerEntity.__init__(self, key,
                                      "127.0.0.1",
                                      5000,
                                      "UpdaterTCPServer")
