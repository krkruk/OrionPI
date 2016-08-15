from bin.Settings.SettingsEntity import SettingsEntity


class SettingsUpdaterEntity(SettingsEntity):
    FILENAME = "filename"
    MODE = "mode"
    COMPRESSION = "compression"
    ALLOW_ZIP_64 = "allowZip64"
    PATH = "path"
    MEMBERS = "members"
    PWD = "pwd"

    def __init__(self, key):
        SettingsEntity.__init__(self, key)
        self.default_settings = {
            self.FILENAME: "update.zip"
        }
