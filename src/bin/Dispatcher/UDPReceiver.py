from circuits import BaseComponent, handler
from bin.Dispatcher.IO.UDPEntity import UDPEntity
from bin.Dispatcher.DataController import *
from .IO.IO import IOStream


class EventlessUDPReceiver(IOStream):
    def __init__(self, controller=Controller(), udp_conn={}, **kwargs):
        self._controller = controller
        self.recent_caller_address = tuple()

    def on_read_line(self, *args, **kwargs):
        try:
            address = args[0]
            msg = args[1]
        except IndexError:
            return
        self.recent_caller_address = address
        self._controller.acquire_new_data(msg)


class UDPReceiver(BaseComponent, EventlessUDPReceiver):
    def __init__(self, controller=Controller(), udp_conn={}, **kwargs):
        BaseComponent.__init__(self)
        EventlessUDPReceiver.__init__(self, controller, udp_conn, **kwargs)
        self.udp = UDPEntity(**udp_conn).register(self)

    @handler("line_read", channel="UDPServer")
    def on_read_line(self, *args, **kwargs):
        EventlessUDPReceiver.on_read_line(self, *args, **kwargs)

    def write_line(self, line, *args, **kwargs):
        self.udp.write_line(line, *args, **kwargs)
