from bin.Updater.DataAssembly import *
import unittest
import hashlib
import random


class TestDataAssebly(unittest.TestCase):
    def setUp(self):
        self.data_assembly = DataAssembly()

        self.single_package = b"0123456789"

    def test_single_package_assembly(self):
        bytesize = len(self.single_package)
        md5sum = hashlib.md5(self.single_package).hexdigest()
        self.data_assembly.init_assembly_params(bytesize, md5sum)
        self.data_assembly.append_bytes(self.single_package)
        if self.data_assembly.can_read():
            data = self.data_assembly.read_data()
            self.assertEqual(self.single_package, data)
        else:
            self.fail("Cannot read data")

    def test_multiple_package_assembly(self):
        data = bytearray()
        md5 = hashlib.md5()
        single_package = bytearray(self.single_package)
        for i in range(random.randrange(300)):
            random.shuffle(single_package)
            data.extend(single_package)
            md5.update(single_package)
        bytesize = len(data)
        md5sum = md5.hexdigest()
        self.data_assembly.init_assembly_params(bytesize, md5sum)
        self.data_assembly.data = data.copy()
        if self.data_assembly.can_read():
            read_data = self.data_assembly.read_data()
            self.assertEqual(data, read_data)
        else:
            self.fail("Cannot read data")

if __name__ == "__main__":
    unittest.main()
