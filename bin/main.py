import src.bin.Dispatcher.UDPReceiver as UDPReceiver
from src.bin.Dispatcher.Devices.Propulsion.PropulsionManager import Propulsion, PropulsionManager
from src.bin.Dispatcher.Devices.DeviceAbstract import NullDevice
from src.bin.Dispatcher.DataController import DataController
from circuits import BaseComponent, handler, Debugger

udp_conn = {"bind": ("127.0.0.1", 3333), "channel": "UDPServer"}
mega_conn = {"port": "/dev/ttyACM0", "channel": "propulsion"}


class Main(BaseComponent):
    def __init__(self):
        super(Main, self).__init__()
        self.propulsion_manager = PropulsionManager(mega_conn).register(self)
        self.propulsion = Propulsion(device_manager=self.propulsion_manager)
        self.controller = DataController(self.propulsion, NullDevice(), NullDevice())
        self.server = UDPReceiver.UDPReceiver(controller=self.controller,
                                              udp_conn=udp_conn).register(self)


if __name__ == "__main__":
    (Main() + Debugger()).run()
