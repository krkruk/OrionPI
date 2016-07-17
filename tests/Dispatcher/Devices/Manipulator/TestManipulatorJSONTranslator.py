from src.bin.Dispatcher.Devices.Manipulator.ManipulatorJSONTranslator import *
import unittest


class TestRPiToManipulatorTranslator(unittest.TestCase):
    def setUp(self):
        self.dict_from_pc = {
            ManipulatorKeysPC.TURRET: ManipulatorDefaultValues.TURRET,
            ManipulatorKeysPC.SHOULDER_LOWER_ACTUATOR: ManipulatorDefaultValues.SHOULDER_LOWER_ACTUATOR,
            ManipulatorKeysPC.ELBOW_UPPER_ACTUATOR: ManipulatorDefaultValues.ELBOW_UPPER_ACTUATOR,
            ManipulatorKeysPC.WRIST_UP_DOWN: ManipulatorDefaultValues.WRIST_UP_DOWN,
            ManipulatorKeysPC.WRIST_ROTATION: ManipulatorDefaultValues.WRIST_ROTATION,
            ManipulatorKeysPC.GRIPPER_GEOMETRY: ManipulatorDefaultValues.GRIPPER_GEOMETRY,
            ManipulatorKeysPC.GRIPPER_GRASPING: ManipulatorDefaultValues.GRIPPER_GRASPING[ManipulatorKeysUC.TOP_FINGER]
        }
        self.expected_uc_dict = {
            ManipulatorKeysUC.TURRET: ManipulatorDefaultValues.TURRET,
            ManipulatorKeysUC.SHOULDER_LOWER_ACTUATOR: ManipulatorDefaultValues.SHOULDER_LOWER_ACTUATOR,
            ManipulatorKeysUC.ELBOW_UPPER_ACTUATOR: ManipulatorDefaultValues.ELBOW_UPPER_ACTUATOR,
            ManipulatorKeysUC.WRIST_UP_DOWN: ManipulatorDefaultValues.WRIST_UP_DOWN,
            ManipulatorKeysUC.WRIST_ROTATION: ManipulatorDefaultValues.WRIST_ROTATION,
            ManipulatorKeysUC.GRIPPER_GEOMETRY: ManipulatorDefaultValues.GRIPPER_GEOMETRY,
            ManipulatorKeysUC.GRIPPER_GRASPING[ManipulatorKeysUC.TOP_FINGER]: ManipulatorDefaultValues.GRIPPER_GRASPING[ManipulatorKeysUC.TOP_FINGER],
            ManipulatorKeysUC.GRIPPER_GRASPING[ManipulatorKeysUC.LEFT_FINGER]: ManipulatorDefaultValues.GRIPPER_GRASPING[ManipulatorKeysUC.LEFT_FINGER],
            ManipulatorKeysUC.GRIPPER_GRASPING[ManipulatorKeysUC.RIGHT_FINGER]: ManipulatorDefaultValues.GRIPPER_GRASPING[ManipulatorKeysUC.RIGHT_FINGER]
        }

    def test_translate_to_uc(self):
        translator = ManipulatorJSONTranslatorRPiToManipulator()
        translated = translator.translate_to_uc(self.dict_from_pc)
        self.assertDictEqual(self.expected_uc_dict, translated)


if __name__ == "__main__":
    unittest.main()