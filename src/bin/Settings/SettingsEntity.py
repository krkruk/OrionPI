class SettingsEntity:
    def __init__(self, key):
        if isinstance(key, str):
            self.key = key
        else:
            raise TypeError("")

        self.settings = {}
        self.default_settings = {}

    def add_entry(self, key, entry):
        self.settings[key] = entry

    def add_entries(self, entries_dict):
        if isinstance(entries_dict, dict):
            self.settings.update(entries_dict)
        else:
            raise TypeError("entries_dict not a dict type")

    def get_entry(self, key):
        entry = self.settings.get(key, None)
        if not entry:
            entry = self.default_settings.get(key)
        return entry

    def get_settings_entity_dict(self):
        entity_settings = self.settings if self.settings else self.default_settings
        return {self.key: entity_settings}

    def get_settings(self):
        return self.settings if self.settings else self.default_settings

    def __getitem__(self, item):
        return self.get_entry(item)

    def __setitem__(self, key, value):
        self.settings[key] = value

    def __eq__(self, other):
        if not isinstance(other, SettingsEntity):
            return False
        if (self.key == other.key and self.settings == other.settings and
                    self.default_settings == other.default_settings):
            return True
        else:
            return False


def get_settings_entity_from_list(entities, settings_keys_to_find):
    for entity in entities:
        if entity.key == settings_keys_to_find:
            return entity
    else:
        return None


class SettingsServerEntity(SettingsEntity):
    IP = "IP"
    PORT = "port"
    CHANNEL = "channel"
    BIND = "bind"

    def __init__(self, key, dflt_ip, dflt_port, dflt_channel):
        SettingsEntity.__init__(self, key)
        self.default_settings = {
            self.IP: dflt_ip,
            self.PORT: dflt_port,
            self.CHANNEL: dflt_channel
        }

    def get_settings(self):
        loaded_settings = SettingsEntity.get_settings(self)
        settings = {self.BIND: (loaded_settings.get(self.IP),
                                loaded_settings.get(self.PORT)),
                    self.CHANNEL: loaded_settings.get(self.CHANNEL)}
        return settings

    def __eq__(self, other):
        if not isinstance(other, SettingsEntity):
            return False
        if (self.key == other.key and self.settings == other.settings and
                    self.default_settings == other.default_settings):
            return True
        else:
            return False