from circuits.net.sockets import UDPServer
from bin.IO import IOStream, line_read
from circuits.net.events import error
from bin.Utility import LineWriter
from bin.Utility import LineReader
from circuits import handler
import logging


class UDPEntity(UDPServer, IOStream):
    def __init__(self, bind, secure=False, backlog=5000, bufsize=4096,
                 channel='server', terminator="\r\n", encoding="utf-8", **kwargs):
        super(UDPEntity, self).__init__(bind, secure, backlog, bufsize, channel, **kwargs)
        self.channel = channel
        self._line_reader = LineReader(terminator, encoding)
        self._line_writer = LineWriter(terminator, encoding)
        self.recv_addr = tuple()

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
        Output: ( (IP, port), string_line )"""
        try:
            self.recv_addr = args[0]
            msg = args[1]
        except IndexError:
            return
        self._line_reader.append_data(msg)
        line = self._line_reader.read_line()

        if line:
            self.fireEvent(line_read(self.recv_addr, line), self.channel)

    @handler("error")
    def on_error(self, *args, **kwargs):
        try:
            sock = args[0]
            err = args[1]
        except IndexError:
            sock = ""
            err = ""

        logging.error("UDP ERROR on socket: {}; Err: {}".format(sock, err))

    def write_line(self, line, *args, **kwargs):
        """Writes a line of bytes and sends it over the network.
        If address is not specified it tries to send a dgram to
        the latest sender address.
        If no message was received the on_error handler is fired."""
        dgram = self._line_writer.write_line(line)
        address = kwargs["address"] if "address" in kwargs else None
        if address:
            self.write(address, dgram)
        elif self.recv_addr:
            self.write(self.recv_addr, dgram)
        else:
            self.fireEvent(error(self.recv_addr, "No address specified!"), self.channel)
