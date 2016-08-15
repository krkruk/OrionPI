import pathlib
import zipfile
import os
import sys


class UpdaterAlgorithmInterface:
    def check_file_exists(self, *args, **kwargs):
        raise NotImplemented()

    def check_file_properties(self, *args, **kwargs):
        raise NotImplemented()

    def decompress(self, *args, **kwargs):
        raise NotImplemented()

    def erase_update_file(self):
        raise NotImplemented()


class UpdaterInterface:
    def update(self):
        raise NotImplemented()

    def clear_update_file(self):
        raise NotImplemented()

    def restart_all(self):
        raise NotImplemented()


class UpdaterZIP(UpdaterAlgorithmInterface):
    def __init__(self, filename, zip_settings={}, *args, **kwargs):
        """
        :param filename: file name with an extension. May contain a directory
        :param zip_settings: All required params required by ZipFile __init__
        and ZipFile.extractall()
        """
        self.filename = pathlib.Path(filename)
        self.settings = {}

    def check_file_exists(self, *args, **kwargs):
        return self.filename.is_file()

    def check_file_properties(self, *args, **kwargs):
        return zipfile.is_zipfile(str(self.filename))

    def decompress(self, *args, **kwargs):
        if not self._can_decompress_file():
            print("Cannot decompress")
            return False

        try:
            return self._open_and_process_zip_file()
        except RuntimeError:
            return False

    def erase_update_file(self):
        if self.check_file_exists():
            os.remove(str(self.filename))

    def _can_decompress_file(self):
        return self.check_file_properties() and self.check_file_exists()

    def _open_and_process_zip_file(self, *args, **kwargs):
        with zipfile.ZipFile(file=str(self.filename), **self.settings) as file:
            if file.testzip():
                return False

            file.extractall(**self.settings)
        return True


class Updater(UpdaterInterface):
    def __init__(self, updater_algorithm=UpdaterAlgorithmInterface()):
        self.update_algorithm = updater_algorithm

    def update(self):
        return self.update_algorithm.decompress()

    def clear_update_file(self):
        self.update_algorithm.erase_update_file()

    @staticmethod
    def restart_all(self):
        interpreter = sys.executable
        app = sys.argv
        os.execl(interpreter, interpreter, *app)
