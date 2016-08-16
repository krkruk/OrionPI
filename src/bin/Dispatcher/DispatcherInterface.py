class DispatcherInterface:
    def register_device(self, obj):
        raise NotImplemented()

    def remove_device(self, obj):
        raise NotImplemented()

    def notify_all(self, *args, **kwargs):
        raise NotImplemented()


class DataDispatcher(DispatcherInterface):
    def __init__(self):
        self.devices = []

    def register_device(self, obj):
        self.devices.append(obj)

    def remove_device(self, obj):
        self.devices.remove(obj)

    def notify_all(self, *args, **kwargs):
        for device in self.devices:
            device.update(*args, **kwargs)
