from bin.IO import IOStream, line_read
from circuits.io.serial import Serial
import bin.Utility as LineWriter
import bin.Utility as LineReader
from circuits import handler


class SerialEntity(Serial, IOStream):
    def __init__(self, port, baudrate=115200, bufsize=4096, timeout=0.2,
                 channel='serial', terminator="\r\n", encoding="utf-8",):
        super(SerialEntity, self).__init__(port, baudrate, bufsize, timeout, channel)
        self.channel = channel
        self._line_reader = LineReader.LineReader(terminator, encoding)
        self._line_writer = LineWriter.LineWriter(terminator, encoding)

    @handler("connected")
    def on_connected(self, *args, **kwargs):
        pass

    @handler("disconnected")
    def on_disconnected(self, *args, **kwargs):
        pass

    @handler("read")
    def on_read(self, *args, **kwargs):
        """Reads a line of data from the buffer.
        Every single line should end up with a terminator specified at init.
        If a new line is received, line_read event is triggered.
        Output: string_line"""
        msg = args[0]
        self._line_reader.append_data(msg)
        line = self._line_reader.read_line()

        if line:
            self.fireEvent(line_read(line), self.channel)

    @handler("error")
    def on_error(self, *args, **kwargs):
        print("SERIAL ERROR:", *args)

    def write_line(self, line, *args, **kwargs):
        """Writes a line of bytes and sends it over the serial."""
        data = self._line_writer.write_line(line)
        self.write(data)
