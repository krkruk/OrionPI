from bin.Updater.UpdaterTransmissionNegotiation import *
from bin.Updater.DataAssembly import DataAssembly, DataAssemblyInterface
from bin.Dispatcher.utility.LineReader import LineReader
from bin.Dispatcher.utility.LineWriter import LineWriter
alias_TN = TransmissionNegotiation


class FileTransferProtocolInterface:
    def run(self, data):
        raise NotImplemented()


class FileTransferProtocol(FileTransferProtocolInterface):
    class MODE:
        NEGOTIATE = 0
        GET_DATA = 1

    def __init__(self, negotiator=TransmissionNegotiationInterface(),
                 data_assembly=DataAssemblyInterface(),
                 data_processor=None,
                 terminator="\r\n", encoding="utf-8",
                 stdio=lambda io: io, stderr=lambda cerr: cerr):
        self._line_reader = LineReader(terminator, encoding)
        self._line_writer = LineWriter(terminator, encoding)
        self.negotiator = negotiator
        self.data_assembly = data_assembly
        self.mode = self.MODE.NEGOTIATE
        self.stdio = stdio
        self.stderr = stderr
        self.ack = None
        self.data_processor = data_processor

    def is_current_mode(self, mode):
        return self.mode == mode

    def set_current_mode(self, mode):
        self.mode = mode

    def run(self, data):
        if self.is_current_mode(self.MODE.NEGOTIATE):
            self.negotiate(data)
        elif self.is_current_mode(self.MODE.GET_DATA):
            self.assemble_data(data)

    def negotiate(self, data):
        line = self._parse_negotiation_data(data)
        if not line:
            return

        self.ack = self.negotiator.negotiate(line)
        if self.ack:
            self._init_assembly_params()
            self.set_current_mode(self.MODE.GET_DATA)
            self._handle_acknowledgement()

    def assemble_data(self, raw_data):
        self.data_assembly.append_bytes(raw_data)
        if self.data_assembly.can_read():
            self._process_recvd_data()
        elif self._has_more_bytes_than_it_should():
            self._handle_error("To much data. Retry!")

    def _parse_negotiation_data(self, data):
        self._line_reader.append_data(data)
        return self._line_reader.read_line()

    def _init_assembly_params(self):
        bytesize = self.ack.results(alias_TN.ACK, alias_TN.FILE_SIZE)
        md5sum = self.ack.results(alias_TN.ACK, alias_TN.MD5)
        self.data_assembly.init_assembly_params(bytesize, md5sum)

    def _handle_acknowledgement(self):
        ack = self.ack.results()
        try:
            ack = ack if isinstance(ack, str) else json.dumps(ack)
        except json.JSONDecodeError:
            self._handle_error("Could not encode ack")
            return

        self.stdio(ack)

    def _process_recvd_data(self):
        print(self.data_assembly.read_data())
        self._reinit()

    def _has_more_bytes_than_it_should(self):
        return self.data_assembly.bytes_size()\
               > self.ack.results(alias_TN.ACK, alias_TN.FILE_SIZE)

    def _handle_error(self, error_text):
        error_json = self.negotiator.create_msg_to_host(error_text)
        self.stderr(error_json)
        self._reinit()

    def _reinit(self):
        self._line_reader.clear()
        self.data_assembly.clear()
        self.set_current_mode(self.MODE.NEGOTIATE)
        self.ack = None
