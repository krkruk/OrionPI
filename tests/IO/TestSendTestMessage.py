import socket


class UDP:
    def __init__(self, bind=("127.0.0.1", 4444)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(bind)

    def send_test_message(self, msg=b"test message", destination=("127.0.0.1", 3333)):
        self.sock.sendto(msg, destination)


if __name__ == "__main__":
    import sys
    """input data:
    * IP address as string
    * destination port
    * msg
    """

    user_entry = True
    try:
        user_data = ((sys.argv[1], int(sys.argv[2])), sys.argv[3])
    except IndexError:
        user_entry = False

    udp = UDP()

    if user_entry:
        destination = user_data[0]
        msg = user_data[1].encode("ascii")
        msg = msg.replace(b"\\r\\n", b"\r\n")
        udp.send_test_message(msg, destination)
    else:
        udp.send_test_message()