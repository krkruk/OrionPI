import hashlib


class DataAssemblyInterface:
    def init_assembly_params(self, bytesize, md5sum):
        raise NotImplemented()

    def append_bytes(self, bytes):
        raise NotImplemented()

    def can_read(self):
        raise NotImplemented()

    def read_data(self):
        raise NotImplemented()

    def bytes_size(self):
        raise NotImplemented()


class DataAssembly(DataAssemblyInterface):
    def __init__(self, bytesize=512, md5sum=""):
        self.bytesize = bytesize
        self.md5sum = md5sum
        self.data = bytearray()

    def init_assembly_params(self, bytesize, md5sum):
        self.data.clear()
        self.bytesize = bytesize
        self.md5sum = md5sum

    def append_bytes(self, bytes):
        self.data.extend(bytes)

    def can_read(self):
        return self._check_bytesize_equal() and self._check_md5_equal()

    def read_data(self):
        return bytes(self.data)

    def bytes_size(self):
        return len(self.data)

    def _check_bytesize_equal(self):
        return self.bytesize == len(self.data)

    def _check_md5_equal(self):
        return self.md5sum == hashlib.md5(self.data).hexdigest()
