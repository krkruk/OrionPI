import src.bin.Dispatcher.utility.LineWriter as LineWriter
import unittest


class TestLineWriter(unittest.TestCase):
    def setUp(self):
        self.str_no_terminator = "no terminator"
        self.byte_no_terminator = b"no terminator"
        self.byte_result_no_terminator = b"no terminator\r\n"

        self.str_with_terminator = "with terminator\r\n"
        self.byte_with_terminator = b"with terminator\r\n"
        self.byte_result_with_terminator = b"with terminator\r\n"

    def test_line_writer_string_no_terminator(self):
        lw = LineWriter.LineWriter()
        line = lw.write_line(self.str_no_terminator)
        self.assertEqual(self.byte_result_no_terminator, line)

    def test_line_writer_byte_no_terminator(self):
        lw = LineWriter.LineWriter()
        line = lw.write_line(self.byte_no_terminator)
        self.assertEqual(self.byte_result_no_terminator, line)

    def test_line_writer_string_with_terminator(self):
        lw = LineWriter.LineWriter()
        line = lw.write_line(self.str_with_terminator)
        self.assertEqual(self.byte_result_with_terminator, line)

    def test_line_writer_byte_with_terminator(self):
        lw = LineWriter.LineWriter()
        line = lw.write_line(self.byte_with_terminator)
        self.assertEqual(self.byte_result_with_terminator, line)

if __name__ == "__main__":
    unittest.main()
