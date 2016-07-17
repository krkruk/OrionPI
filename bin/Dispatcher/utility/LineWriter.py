from .LineProcessing import LineProcessing


class LineWriter(LineProcessing):
    def __init__(self, terminator="\r\n", encoding="utf-8"):
        super(LineWriter, self).__init__(terminator, encoding)

    def write_line(self, line_of_data):
        """Converts a line of data into a string of bytes
        ended with TERMINATOR."""
        line_of_bytes = line_of_data.encode(self.ENCODING) \
            if isinstance(line_of_data, str) else line_of_data
        return line_of_bytes \
            if self.TERMINATOR in line_of_bytes else line_of_bytes + self.TERMINATOR

