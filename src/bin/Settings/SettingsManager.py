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
            json.dump(data, file, indent=4)

    def load(self):
        if not os.path.isfile(self.filename):
            self.save()
            return

        with open(self.filename, 'r', encoding="utf-8") as file:
            try:
                json_dict = json.load(file)
            except json.JSONDecodeError:
                return

        for entity in self.entities:
            if entity.key in json_dict:
                entity.add_entries(json_dict[entity.key])


class SettingsLoader:
    def __init__(self, filename, create_parameters):
        assert isinstance(create_parameters, dict)
        self.filename = filename
        self.json_dict_data = {}
        self.create_parameters = create_parameters

    def load(self):
        if not self._file_exists():
            return []

        self.json_dict_data = self._open_file_get_json_dict()
        return self._split_to_settings_entity()

    def _file_exists(self):
        return os.path.isfile(self.filename)

    def _open_file_get_json_dict(self):
        with open(self.filename, 'r', encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}

    def _split_to_settings_entity(self):
        entities = []
        for key in self.json_dict_data.keys():
            entity = self._create_entity(key)
            entity.add_entries(self.json_dict_data[key].copy())
            entities.append(entity)
        return entities

    def _create_entity(self, key):
        entity_class = self.create_parameters.get(key, SettingsEntity)
        return entity_class(key)
