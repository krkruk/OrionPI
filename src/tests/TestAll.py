from tests.Dispatcher.TestDispatchingSystem import *
from tests.Dispatcher.Devices.TestDeviceManagerFactory import *
from tests.Dispatcher.Devices.TestDeviceWholesale import *
from tests.Dispatcher.Devices.Manipulator.TestManipulatorFactory import *
from tests.Dispatcher.Devices.Manipulator.TestManipulatorJSONTranslator import *
from tests.Dispatcher.Devices.Propulsion.TestPropulsionFactory import *
from tests.Dispatcher.Settings.TestSettings import *
from tests.Dispatcher.Settings.TestSettingsManager import *
from tests.Dispatcher.Settings.TestSettingsLoader import *
from tests.Dispatcher.utility.TestLineReader import *
from tests.Dispatcher.utility.TestLineWriter import *
from tests.Updater.TestUpdaterTransmissionNegotiation import *
from tests.Updater.TestDataAssembly import *
from tests.Updater.TestUpdaterTCPServer import *
import unittest


if __name__ == "__main__":
    unittest.main()
