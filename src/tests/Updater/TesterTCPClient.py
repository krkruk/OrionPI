"""
This code is used for sending TCP messages to UpdaterTCPServer. It is
a part of testing the server 'by hand'. Real tests will be performed by
TestUpdaterTCPServer and will be based on Mock objects
"""

from circuits.net.sockets import TCPClient, connect, disconnect
from circuits import Debugger, handler, Event
from circuits import Timer
import hashlib
import json


data = b"MyData. Hello world!"
md5_data = hashlib.md5(data).hexdigest()
data_size = len(data)
data_dict = {
    "SYN": {
        "filename": "update.txt",
        "filesize": data_size,
        "MD5": md5_data
    }
}
cmd_json = json.dumps(data_dict) + "\r\n"
cmd_bin = cmd_json.encode()


with open("test.zip", "br") as file:
    file_data = file.read()

file_md5 = hashlib.md5(file_data).hexdigest()
file_size = len(file_data)
file_dict = {
    "SYN": {
        "filename": "update.zip",
        "filesize": file_size,
        "MD5": file_md5
    }
}
file_cmd_json = json.dumps(file_dict) + "\r\n"
file_cmd_bin = file_cmd_json.encode()


class Send(TCPClient):
    @handler("started")
    def started(self, *args, **kwargs):
        self.init()
        self.fireEvent(connect("127.0.0.1", 5000))
        Timer(1, Event.create("write_data")).register(self)

    @handler("connected")
    def on_connected(self, *args, **kwargs):
        print(*args)

    @handler("write_data")
    def on_write_data(self, *args, **kwargs):
        print("Write request!!!", cmd_bin)
        self.write(cmd_bin)

    @handler("read")
    def on_read(self, *args):
        print(args)
        parsed_data = json.loads(args[0].decode())
        if parsed_data.get("ACK"):
            print("Write data!!!", data)
            self.write(data)
        if parsed_data.get("info"):
            print(parsed_data.get("info"))
            Timer(1, disconnect()).register(self)

    @handler("disconnect")
    def on_kill(self, *args, **kwargs):
        print("KILLLLL!!!")
        raise SystemExit(1)


class SendFile(TCPClient):
    @handler("started")
    def started(self, *args, **kwargs):
        self.init()
        self.fireEvent(connect("127.0.0.1", 5000))
        Timer(1, Event.create("write_data")).register(self)

    @handler("connected")
    def on_connected(self, *args, **kwargs):
        print(*args)

    @handler("write_data")
    def on_write_data(self, *args, **kwargs):
        print("Write request!!!", file_cmd_bin)
        self.write(file_cmd_bin)

    @handler("read")
    def on_read(self, *args):
        print(args)
        parsed_data = json.loads(args[0].decode())
        if parsed_data.get("ACK"):
            print("Write data!!!", file_data)
            self.write(file_data)
        if parsed_data.get("info"):
            print(parsed_data.get("info"))
            Timer(1, disconnect()).register(self)

    @handler("disconnect")
    def on_kill(self, *args, **kwargs):
        print("KILLLLL!!!")
        raise SystemExit(1)


if __name__ == "__main__":
    import random
    app = SendFile(("127.0.0.1", random.randint(5001, 10000)))
    app.run()
    import os
    pid = os.getpid()
    import subprocess
    subprocess.run(["kill", str(pid)])
