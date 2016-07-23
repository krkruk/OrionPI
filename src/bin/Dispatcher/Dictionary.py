class DeviceClass:
    PROPULSION = "CPR"
    MANIPULATOR = "CMR"
    PERIPHERIES = "CPS"


class SettingsKeys:
    PROPULSION = "PROPULSION"
    MANIPULATOR = "MANIPULATOR"
    PERIPHERIES = "PERIPHERIES"
    UDP = "UDP"


class PropulsionKeys:
    LEFT_WHEEL_SPEED = "LWS"
    RIGHT_WHEEL_SPEED = "RWS"


class ManipulatorKeysPC:
    TURRET = "TRT"
    SHOULDER_LOWER_ACTUATOR = "SLA"
    ELBOW_UPPER_ACTUATOR = "EUA"
    WRIST_UP_DOWN = "WUD"
    WRIST_ROTATION = "WRN"
    GRIPPER_GEOMETRY = "GGY"
    GRIPPER_GRASPING = "GGG"


class ManipulatorKeysUC:
    TURRET = "RotationArmMotor"
    SHOULDER_LOWER_ACTUATOR = "BaseDownArmMotor"
    ELBOW_UPPER_ACTUATOR = "BaseMidArmMotor"
    WRIST_UP_DOWN = "BaseUpArmMotor"
    WRIST_ROTATION = "GrasperRotationArmMotor"
    GRIPPER_GEOMETRY = "GeometryArmServo"
    TOP_FINGER = "TOP_FINGER"
    LEFT_FINGER = "LEFT_FINGER"
    RIGHT_FINGER = "RIGHT_FINGER"
    GRIPPER_GRASPING = {
        TOP_FINGER: "UpArmServo",
        LEFT_FINGER: "LeftArmServo",
        RIGHT_FINGER: "RightArmServo"
    }


class ManipulatorDefaultValues:
    TURRET = 0
    SHOULDER_LOWER_ACTUATOR = 0
    ELBOW_UPPER_ACTUATOR = 0
    WRIST_UP_DOWN = 0
    WRIST_ROTATION = 0
    GRIPPER_GEOMETRY = 90
    FINGER_AVERAGE = "FINGER_AVERAGE"
    GRIPPER_GRASPING = {
        ManipulatorKeysUC.TOP_FINGER: 90,
        ManipulatorKeysUC.LEFT_FINGER: 90,
        ManipulatorKeysUC.RIGHT_FINGER: 90,
        FINGER_AVERAGE: 90
    }
