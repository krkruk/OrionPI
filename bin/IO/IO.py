from circuits import Event


class line_read(Event):
    pass


class IOStream:
    def on_connected(self, *args, **kwargs):
        raise NotImplemented()

    def on_disconnected(self, *args, **kwargs):
        raise NotImplemented()

    def on_read(self, *args, **kwargs):
        raise NotImplemented()

    def on_error(self, *args, **kwargs):
        raise NotImplemented()

    def write_line(self, line, *args, **kwargs):
        raise NotImplemented()
