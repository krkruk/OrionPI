import pathlib


class UpdaterDataProcessorInterface:
    def process(self, raw_data):
        raise NotImplemented()

    def save(self, filename, mode="bw"):
        raise NotImplemented()


class UpdaterDataProcessor(UpdaterDataProcessorInterface):
    """
    UpdaterDataProcessor allows storing the data into given directory,
    by default in a binary mode.

    The data is save() in a given directory at given filename,
    however must be process()-ed beforehand.
    The object is cleaned after saving the data.
    """
    def __init__(self, directory="./"):
        self.directory = directory
        self.raw_data = bytes()
        self.filename = ""

    def process(self, raw_data):
        self.raw_data = raw_data

    def save(self, filename, mode="bw"):
        self.filename = filename

        self._save_data(mode)
        self._clean_up()

    def _save_data(self, mode):
        save_to = self._generate_path()
        with open(str(save_to), mode) as file:
            file.write(self.raw_data)

    def _clean_up(self):
        self.raw_data = bytes()
        self.filename = ""

    def _generate_path(self):
        return pathlib.Path(self.directory, self.filename)
