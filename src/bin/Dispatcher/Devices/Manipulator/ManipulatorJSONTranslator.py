from bin.Dispatcher.Dictionary import *


class ManipulatorJSONTranslatorAbstract:
    def __init__(self):
        self.data = {}
        self.translated = {}

    def translate_to_pc(self, data):
        self.data = data
        self.translate_turret()
        self.translate_shoulder_lower_actuator()
        self.translate_elbow_upper_actuator()
        self.translate_wrist_up_down()
        self.translate_wrist_rotation()
        self.translate_gripper_geometry()
        self.translate_gripper_grasping()
        return self.translated

    def translate_to_uc(self, data):
        self.data = data
        self.translate_turret()
        self.translate_shoulder_lower_actuator()
        self.translate_elbow_upper_actuator()
        self.translate_wrist_up_down()
        self.translate_wrist_rotation()
        self.translate_gripper_geometry()
        self.translate_gripper_grasping()
        return self.translated

    def translate_turret(self):
        raise NotImplemented()

    def translate_shoulder_lower_actuator(self):
        raise NotImplemented()

    def translate_elbow_upper_actuator(self):
        raise NotImplemented()

    def translate_wrist_up_down(self):
        raise NotImplemented()

    def translate_wrist_rotation(self):
        raise NotImplemented()

    def translate_gripper_geometry(self):
        raise NotImplemented()

    def translate_gripper_grasping(self):
        raise NotImplemented()

    def translate_top_finger(self, *args):
        raise NotImplemented()

    def translate_left_finger(self, *args):
        raise NotImplemented()

    def translate_right_finger(self, *args):
        raise NotImplemented()


class ManipulatorJSONTranslatorRPiToManipulator(ManipulatorJSONTranslatorAbstract):
    def __init__(self):
        super(ManipulatorJSONTranslatorRPiToManipulator, self).__init__()

    def translate_to_pc(self, data):
        pass

    def translate_turret(self):
        self.translated[ManipulatorKeysUC.TURRET] \
            = self.data.get(ManipulatorKeysPC.TURRET,
                            ManipulatorDefaultValues.TURRET)

    def translate_shoulder_lower_actuator(self):
        self.translated[ManipulatorKeysUC.SHOULDER_LOWER_ACTUATOR] \
            = self.data.get(ManipulatorKeysPC.SHOULDER_LOWER_ACTUATOR,
                            ManipulatorDefaultValues.SHOULDER_LOWER_ACTUATOR)

    def translate_elbow_upper_actuator(self):
        self.translated[ManipulatorKeysUC.ELBOW_UPPER_ACTUATOR] \
            = self.data.get(ManipulatorKeysPC.ELBOW_UPPER_ACTUATOR,
                            ManipulatorDefaultValues.ELBOW_UPPER_ACTUATOR)

    def translate_wrist_up_down(self):
        self.translated[ManipulatorKeysUC.WRIST_UP_DOWN] \
            = self.data.get(ManipulatorKeysPC.WRIST_UP_DOWN,
                            ManipulatorDefaultValues.WRIST_UP_DOWN)

    def translate_wrist_rotation(self):
        self.translated[ManipulatorKeysUC.WRIST_ROTATION] \
            = self.data.get(ManipulatorKeysPC.WRIST_ROTATION,
                            ManipulatorDefaultValues.WRIST_ROTATION)

    def translate_gripper_geometry(self):
        self.translated[ManipulatorKeysUC.GRIPPER_GEOMETRY] \
            = self.data.get(ManipulatorKeysPC.GRIPPER_GEOMETRY,
                            ManipulatorDefaultValues.GRIPPER_GEOMETRY)

    def translate_gripper_grasping(self):
        grasping_value \
            = self.data.get(ManipulatorKeysPC.GRIPPER_GRASPING,
                            ManipulatorDefaultValues.GRIPPER_GRASPING[ManipulatorDefaultValues.FINGER_AVERAGE])
        self.translate_top_finger(grasping_value)
        self.translate_left_finger(grasping_value)
        self.translate_right_finger(grasping_value)

    def translate_top_finger(self, *args):
        try:
            value = args[0]
        except IndexError:
            return
        key = ManipulatorKeysUC.GRIPPER_GRASPING[ManipulatorKeysUC.TOP_FINGER]
        self.translated[key] = value

    def translate_left_finger(self, *args):
        try:
            value = args[0]
        except IndexError:
            return
        key = ManipulatorKeysUC.GRIPPER_GRASPING[ManipulatorKeysUC.LEFT_FINGER]
        self.translated[key] = value

    def translate_right_finger(self, *args):
        try:
            value = args[0]
        except IndexError:
            return
        key = ManipulatorKeysUC.GRIPPER_GRASPING[ManipulatorKeysUC.RIGHT_FINGER]
        self.translated[key] = value

if __name__ == "__main__":
    dict_from_pc = {
        ManipulatorKeysPC.TURRET: ManipulatorDefaultValues.TURRET,
        ManipulatorKeysPC.SHOULDER_LOWER_ACTUATOR: ManipulatorDefaultValues.SHOULDER_LOWER_ACTUATOR,
        ManipulatorKeysPC.ELBOW_UPPER_ACTUATOR: ManipulatorDefaultValues.ELBOW_UPPER_ACTUATOR,
        ManipulatorKeysPC.WRIST_UP_DOWN: ManipulatorDefaultValues.WRIST_UP_DOWN,
        ManipulatorKeysPC.WRIST_ROTATION: ManipulatorDefaultValues.WRIST_ROTATION,
        ManipulatorKeysPC.GRIPPER_GEOMETRY: ManipulatorDefaultValues.GRIPPER_GEOMETRY,
        ManipulatorKeysPC.GRIPPER_GRASPING: ManipulatorDefaultValues.GRIPPER_GRASPING[ManipulatorKeysUC.TOP_FINGER]
    }
    expected_uc_dict = {
        ManipulatorKeysUC.TURRET: ManipulatorDefaultValues.TURRET,
        ManipulatorKeysUC.SHOULDER_LOWER_ACTUATOR: ManipulatorDefaultValues.SHOULDER_LOWER_ACTUATOR,
        ManipulatorKeysUC.ELBOW_UPPER_ACTUATOR: ManipulatorDefaultValues.ELBOW_UPPER_ACTUATOR,
        ManipulatorKeysUC.WRIST_UP_DOWN: ManipulatorDefaultValues.WRIST_UP_DOWN,
        ManipulatorKeysUC.WRIST_ROTATION: ManipulatorDefaultValues.WRIST_ROTATION,
        ManipulatorKeysUC.GRIPPER_GEOMETRY: ManipulatorDefaultValues.GRIPPER_GEOMETRY,
        ManipulatorKeysUC.GRIPPER_GRASPING[ManipulatorKeysUC.TOP_FINGER]: ManipulatorDefaultValues.GRIPPER_GRASPING[
            ManipulatorKeysUC.TOP_FINGER],
        ManipulatorKeysUC.GRIPPER_GRASPING[ManipulatorKeysUC.LEFT_FINGER]: ManipulatorDefaultValues.GRIPPER_GRASPING[
            ManipulatorKeysUC.LEFT_FINGER],
        ManipulatorKeysUC.GRIPPER_GRASPING[ManipulatorKeysUC.RIGHT_FINGER]: ManipulatorDefaultValues.GRIPPER_GRASPING[
            ManipulatorKeysUC.RIGHT_FINGER]
    }


    def test_translate_to_uc():
        translator = ManipulatorJSONTranslatorRPiToManipulator()
        translated = translator.translate_to_uc(dict_from_pc)
        print("===PC===\n{}\n\n".format(dict_from_pc))
        print("===Translated===\n{}\n\n".format(translated))
        print("===Expected===\n{}\n\n".format(expected_uc_dict))

    test_translate_to_uc()
