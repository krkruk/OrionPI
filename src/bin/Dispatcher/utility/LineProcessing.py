class LineProcessing:
    def __init__(self, terminator, encoding):
        self.TERMINATOR = terminator.encode() if isinstance(terminator, str) else terminator
        self.ENCODING = str(encoding)

    def write_line(self, line_of_data):
        raise NotImplemented()
