from bin.Updater.UpdaterTransmissionNegotiation import TransmissionNegotiationAbstract
from bin.Updater.DataAssembly import DataAssemblyInterface
from bin.Dispatcher.utility.LineReader import LineReader
from bin.Dispatcher.utility.LineWriter import LineWriter
from bin.Dispatcher.IO.IO import IOStream, line_read
from circuits.net.sockets import TCPServer
from circuits import handler, Debugger
import json


class EventlessUpdaterTCPServer(IOStream):
    class MODE:
        NEGOTIATE = 0
        GET_DATA = 1

    def __init__(self, bind, negotiator=TransmissionNegotiationAbstract(),
                 data_assembly=DataAssemblyInterface(),
                 secure=False, backlog=5000, bufsize=4096, channel='UpdaterTCPServer',
                 terminator="\r\n", encoding="utf-8", **kwargs):
        self.negotiator = negotiator
        self.data_assembly = data_assembly
        self.channel = channel
        self.mode = self.MODE.NEGOTIATE
        self.conn_to_sock = tuple()
        self._line_reader = LineReader(terminator, encoding)
        self._line_writer = LineWriter(terminator, encoding)

    def on_read(self, *args, **kwargs):
        try:
            self.conn_to_sock = args[0]
            data = args[1]
        except IndexError:
            return

        self.mode = self.MODE.GET_DATA

    def write_line(self, line, *args, **kwargs):
        pass


class UpdaterTCPServer(TCPServer, IOStream):
    class MODE:
        NEGOTIATE = 0
        GET_DATA = 1

    def __init__(self, bind, negotiator=TransmissionNegotiationAbstract(),
                 data_assembly=DataAssemblyInterface(),
                 secure=False, backlog=5000, bufsize=4096, channel='UpdaterTCPServer',
                 terminator="\r\n", encoding="utf-8", **kwargs):
        TCPServer.__init__(self, bind, secure, backlog, bufsize, channel, **kwargs)
        self._line_writer = LineWriter(terminator, encoding)
        self._line_reader = LineReader(terminator, encoding)
        self.negotiator = negotiator
        self.data_assembly = data_assembly
        self.sock = tuple()
        self.mode = self.MODE.NEGOTIATE

    @handler("connect", channel="UpdaterTCPServer")
    def on_connected(self, *args, **kwargs):
        print("Connected! {}".format(*args))

    @handler("read", channel="UpdaterTCPServer")
    def on_read(self, *args, **kwargs):
        pass


if __name__ == "__main__":
    from bin.Updater.DataAssembly import DataAssembly
    from bin.Updater.UpdaterTransmissionNegotiation import TransmissionNegotiation
    bind = ("127.0.0.1", 5000)
    data_assembly = DataAssembly()
    negotiator = TransmissionNegotiation()
    (Debugger() + UpdaterTCPServer(bind, negotiator, data_assembly)).run()
