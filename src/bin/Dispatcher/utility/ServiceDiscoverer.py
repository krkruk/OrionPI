from serial.tools import list_ports


def get_port_name(regex):
    for device_info in list_ports.grep(regex):
        return device_info.device
    else:
        return None


if __name__ == "__main__":
    print(get_port_name("/dev/ttyUSB0"))
