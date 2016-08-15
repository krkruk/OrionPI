from bin.Updater.UpdaterTransmissionNegotiation import TransmissionNegotiationInterface, TransmissionNegotiation
from bin.Updater.UpdaterDataProcessor import UpdaterDataProcessor, UpdaterDataProcessorInterface
from bin.Updater.DataAssembly import DataAssemblyInterface, DataAssembly
from bin.Updater.FileTransferProtocol import FileTransferProtocol
from bin.Dispatcher.utility.LineWriter import LineWriter
from circuits.net.sockets import TCPServer
from bin.Dispatcher.IO.IO import IOStream
from bin.Settings import SettingsEntity
from circuits import handler, Debugger
from circuits import Event, Timer


alias_TN = TransmissionNegotiation


class update_acquired(Event):
    """Event is fired only if the data was positively acquired"""


class EventlessUpdaterTCPServer(IOStream):
    class MODE:
        NEGOTIATE = 0
        GET_DATA = 1

    def __init__(self, bind, negotiator=TransmissionNegotiationInterface(),
                 data_assembly=DataAssemblyInterface(),
                 data_processor=UpdaterDataProcessorInterface(),
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
                                        data_processor=data_processor,
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

    def __init__(self, tcp_updater_sett_entity=SettingsEntity(""), **kwargs):
        self.tcp_conn = tcp_updater_sett_entity.get_settings()
        TCPServer.__init__(self, **self.tcp_conn, **kwargs)
        self.negotiator = TransmissionNegotiation()
        self.data_assembly = DataAssembly()
        self.data_processor = UpdaterDataProcessor()
        self.stdio = self.write_line
        self.stderr = self.on_error
        EventlessUpdaterTCPServer.__init__(self, negotiator=self.negotiator,
                                           data_assembly=self.data_assembly,
                                           data_processor=self.data_processor,
                                           stdio=self.stdio, stderr=self.stderr,
                                           **self.tcp_conn, **kwargs)

    @handler("connect", channel="UpdaterTCPServer")
    def on_connected(self, *args, **kwargs):
        print("Connected! {}".format(*args))

    @handler("read", channel="UpdaterTCPServer")
    def on_read(self, *args, **kwargs):
        EventlessUpdaterTCPServer.on_read(self, *args, **kwargs)

    def write_line(self, line, *args, **kwargs):
        data = EventlessUpdaterTCPServer.write_line(self, line, *args, **kwargs)
        self.write(self.conn_to_sock, data)

        self._fire_event_on_data_received_msg(line)

    @handler("error", channel="UpdaterTCPServer")
    def on_error(self, *args, **kwargs):
        EventlessUpdaterTCPServer.on_error(self, *args, **kwargs)

    def _fire_event_on_data_received_msg(self, line):
        if FileTransferProtocol.MSG_DATA_RECVD in line:
            Timer(1, update_acquired()).register(self)


if __name__ == "__main__":
    from bin.Updater.DataAssembly import DataAssembly
    from bin.Updater.UpdaterTransmissionNegotiation import TransmissionNegotiation
    from bin.Settings.SettingsUpdaterTCPServer import SettingsUpdaterTCPServer
    from bin.Dispatcher.Dictionary import *
    settings = SettingsUpdaterTCPServer(SettingsKeys.TCP_UPDATER_SERVER)
    (Debugger() + UpdaterTCPServer(settings)).run()
