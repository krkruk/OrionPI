from src.bin.Dispatcher.utility.LineReader import LineReader
import unittest


class TestLineReader(unittest.TestCase):
    def setUp(self):
        self.binary_single_line = b"myFirstSingleLine\r\n"
        self.string_single_line = "myFirstSingleLine"

        self.binary_array_line = bytearray()
        self.string_single_line_second = "my second single line"
        self.binary_array_line.extend(b"myFirst")
        self.binary_array_line.extend(b"SingleLine")
        self.binary_array_line.extend(b"\r\n")
        self.binary_array_line.extend(b"my second")
        self.binary_array_line.extend(b" single line\r\n")

    def test_convert_bytes_to_string(self):
        reader = LineReader()
        self.assertEqual(self.string_single_line,
                         reader.write_line(self.binary_single_line).rstrip())

    def test_read_line_from_exact_one_line(self):
        reader = LineReader()
        reader.append_data(self.binary_single_line)
        line = reader.read_line()
        self.assertEqual(self.string_single_line, line)

    def test_read_line_from_empty_buffer(self):
        reader = LineReader()
        line = reader.read_line()
        self.assertEqual("", line)

    def test_read_line_two_lines(self):
        reader = LineReader()
        reader.append_data(self.binary_array_line)
        line1 = reader.read_line()
        line2 = reader.read_line()
        self.assertEqual(self.string_single_line_second, line2)

    def test_read_line_try_read_line_until_terminator_entered(self):
        reader = LineReader()
        reader.append_data(self.string_single_line.encode())
        line = reader.read_line()
        self.assertEqual("", line)

    def test_read_line_try_read_line_with_terminator_added_after_calling_read_line(self):
        reader = LineReader()
        reader.append_data(self.string_single_line.encode())
        empty_line_tested_above = reader.read_line()
        reader.append_data("\r\n".encode())
        line = reader.read_line()
        self.assertEqual(self.string_single_line, line)


if __name__ == "__main__":
    unittest.main()
