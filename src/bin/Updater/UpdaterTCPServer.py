from bin.Updater.UpdaterTransmissionNegotiation import TransmissionNegotiationInterface, TransmissionNegotiation
from bin.Updater.FileTransferProtocol import FileTransferProtocol
from bin.Updater.DataAssembly import DataAssemblyInterface
from bin.Dispatcher.utility.LineWriter import LineWriter
from bin.Dispatcher.IO.IO import IOStream
from circuits.net.sockets import TCPServer
from circuits import handler, Debugger

alias_TN = TransmissionNegotiation


class EventlessUpdaterTCPServer(IOStream):
    class MODE:
        NEGOTIATE = 0
        GET_DATA = 1

    def __init__(self, bind, negotiator=TransmissionNegotiationInterface(),
                 data_assembly=DataAssemblyInterface(),
                 data_processor=None,
                 stdio=lambda io: io,
                 stderr=lambda cerr: cerr,
                 secure=False, backlog=5000, bufsize=4096, channel='UpdaterTCPServer',
                 terminator="\r\n", encoding="utf-8", **kwargs):
        self.negotiator = negotiator
        self.data_assembly = data_assembly
        self.channel = channel
        self.conn_to_sock = tuple()
        self._line_writer = LineWriter(terminator, encoding)
        self.ftp = FileTransferProtocol(self.negotiator,
                                        self.data_assembly,
                                        data_processor=None,
                                        terminator=terminator,
                                        encoding=encoding,
                                        stdio=stdio,
                                        stderr=stderr)

    def on_read(self, *args, **kwargs):
        try:
            self.conn_to_sock = args[0]
            data = args[1]
        except IndexError:
            return

        self.ftp.run(data)

    def write_line(self, line, *args, **kwargs):
        return self._line_writer.write_line(line)

    def on_error(self, *args, **kwargs):
        try:
            error_text = args[0]
        except IndexError:
            error_text = "error"
        self.write_line(error_text)


class UpdaterTCPServer(TCPServer, EventlessUpdaterTCPServer):
    class MODE:
        NEGOTIATE = 0
        GET_DATA = 1

    def __init__(self, bind,
                 negotiator=TransmissionNegotiationInterface(),
                 data_assembly=DataAssemblyInterface(),
                 secure=False, backlog=5000, bufsize=4096, channel='UpdaterTCPServer',
                 terminator="\r\n", encoding="utf-8", **kwargs):
        TCPServer.__init__(self, bind, secure, backlog, bufsize, channel, **kwargs)
        self.negotiator = TransmissionNegotiation()
        self.data_assembly = DataAssembly()
        self.data_processor = None
        self.stdio = self.write_line
        self.stderr = self.on_error
        EventlessUpdaterTCPServer.__init__(self, bind, self.negotiator, self.data_assembly,
                                           self.data_processor, self.stdio, self.stderr,
                                           secure, backlog, bufsize, channel, terminator, encoding,
                                           **kwargs)

    @handler("connect", channel="UpdaterTCPServer")
    def on_connected(self, *args, **kwargs):
        print("Connected! {}".format(*args))

    @handler("read", channel="UpdaterTCPServer")
    def on_read(self, *args, **kwargs):
        EventlessUpdaterTCPServer.on_read(self, *args, **kwargs)

    def write_line(self, line, *args, **kwargs):
        data = EventlessUpdaterTCPServer.write_line(self, line, *args, **kwargs)
        self.write(self.conn_to_sock, data)

    @handler("error", channel="UpdaterTCPServer")
    def on_error(self, *args, **kwargs):
        EventlessUpdaterTCPServer.on_error(self, *args, **kwargs)


if __name__ == "__main__":
    from bin.Updater.DataAssembly import DataAssembly
    from bin.Updater.UpdaterTransmissionNegotiation import TransmissionNegotiation
    bind = ("127.0.0.1", 5000)
    data_assembly = DataAssembly()
    negotiator = TransmissionNegotiation()
    (Debugger() + UpdaterTCPServer(bind, negotiator, data_assembly)).run()
