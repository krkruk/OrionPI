from bin.Devices.Manipulator.ManipulatorJSONTranslator import ManipulatorJSONTranslatorRPiToManipulator
from bin.Dispatcher.Dictionary import DeviceClass
from bin.Devices import Device


class Manipulator(Device):
    def __init__(self, device_manager):
        super(Manipulator, self).__init__(DeviceClass.MANIPULATOR, device_manager)
        self.translator = ManipulatorJSONTranslatorRPiToManipulator()

    def handle_data_incoming(self, data={}):
        d = self.translator.translate_to_uc(data)
        return d
