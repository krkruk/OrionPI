from bin.Settings.SettingsEntity import SettingsEntity
import os.path
import json


class SettingsManagerAbstract:
    def __init__(self, filename, entities=[]):
        assert filename and isinstance(filename, str)
        self.filename = filename
        self.entities = entities

    def add_entity(self, entity):
        if isinstance(entity, SettingsEntity):
            self.entities.append(entity)
        elif hasattr(entity, "__iter__"):
            self.entities.extend(entity)

    def save(self):
        raise NotImplemented()

    def load(self):
        raise NotImplemented()


class SettingsManagerMock(SettingsManagerAbstract):
    def __init__(self, filename, entities=[]):
        SettingsManagerAbstract.__init__(self, filename, entities)
        self.settings_data = {}
        self.json_string = ""

    def load(self):
        if self.filename:
            for entity in self.entities:
                default_settings = entity.default_settings
                self.settings_data.update(default_settings)
                entity.add_entries(default_settings)

    def save(self):
        if self.filename:
            data = {}
            for entity in self.entities:
                data.update(entity.get_settings_entity_dict())
            self.json_string = json.dumps(data)


class SettingsManager(SettingsManagerAbstract):
    def __init__(self, filename, entities=[]):
        SettingsManagerAbstract.__init__(self, filename, entities)

    def save(self):
        with open(self.filename, 'w', encoding="utf-8") as file:
            data = {}
            for entity in self.entities:
                data.update(entity.get_settings_entity_dict())
            file.write(json.dumps(data))

    def load(self):
        if not os.path.isfile(self.filename):
            self.save()
            return

        with open(self.filename, 'r', encoding="utf-8") as file:
            string_data = file.read()
        try:
            json_dict = json.loads(string_data)
        except json.JSONDecodeError:
            return

        for entity in self.entities:
            if entity.key in json_dict:
                entity.add_entries(json_dict[entity.key])
