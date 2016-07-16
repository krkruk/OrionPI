import IO.UDPEntity as UDPEntity
import IO.SerialEntity as SerialEntity
from circuits import Component, handler, Debugger


class Main(Component):
    def __init__(self):
        super(Main, self).__init__()
        self.server = UDPEntity.UDPEntity(("127.0.0.1", 3333), channel="UDPServer").register(self)
        self.uno = SerialEntity.SerialEntity("/dev/ttyACM0", channel="uno").register(self)
        self.mega = SerialEntity.SerialEntity("/dev/ttyACM1", channel="mega").register(self)

    def started(self, *args):
        self.server.write_line("hello!", address=("127.0.0.1", 3333))
        self.server.write_line(b"bytes!", address=("127.0.0.1", 3333))

    @handler("line_read", channel="UDPServer")
    def line(self, *args):
        print("In udp:", *args)

    @handler("line_read", channel="uno")
    def serial_line(self, *args):
        print("In Uno: ", *args)
        self.uno.write_line("My Line")

    @handler("line_read", channel="mega")
    def mega_line(self, *args):
        print("In Mega: ", *args)
        self.mega.write_line("My Line")


if __name__ == "__main__":
    (Main() + Debugger()).run()
    # Main().run()