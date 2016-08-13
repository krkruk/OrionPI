"""
This code is used for sending TCP messages to UpdaterTCPServer. It is
a part of testing the server 'by hand'. Real tests will be performed by
TestUpdaterTCPServer and will be based on Mock objects
"""

from circuits.net.sockets import TCPClient, connect, disconnect
from circuits import Debugger, handler, Event
from circuits import Timer


class Send(TCPClient):
    @handler("started")
    def started(self, *args, **kwargs):
        self.init()
        self.fireEvent(connect("127.0.0.1", 5000))
        Timer(1, Event.create("write_data")).register(self)
        # Timer(2, Event.create("kill")).register(self)

    @handler("connected")
    def on_connected(self, *args, **kwargs):
        print(*args)

    @handler("write_data")
    def on_write_data(self, *args, **kwargs):
        print("Write hello world!!!\n")
        self.write(b'{"SYN": {"filename": "update.zip", "MD5": "", "filesize": 30}}\r\n')
        Timer(1, disconnect()).register(self)

    @handler("disconnect")
    def on_kill(self, *args, **kwargs):
        print("KILLLLL!!!")
        raise SystemExit(1)


if __name__ == "__main__":
    import random
    app = Send(("127.0.0.1", random.randint(5001, 10000)))
    app.run()
    import os
    pid = os.getpid()
    import subprocess
    subprocess.run(["kill", str(pid)])
