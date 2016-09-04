class DeviceObservableInterface:
    def notify_all(self, *args, **kwargs):
        raise NotImplemented("")

    def add_observer(self, observer, *args, **kwargs):
        raise NotImplemented("")

    def del_observer(self, observer, *args, **kwargs):
        raise NotImplemented("")


class DeviceObservableAbstract(DeviceObservableInterface):
    def __init__(self):
        self.observers = []

    def add_observer(self, observer, *args, **kwargs):
        if isinstance(observer, list) or isinstance(observer, tuple):
            self.observers.extend(observer)
        else:
            self.observers.append(observer)

    def del_observer(self, observer, *args, **kwargs):
        self.observers.remove(observer)
