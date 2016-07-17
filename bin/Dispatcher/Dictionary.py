class DeviceClass:
    PROPULSION = "CPR"
    MANIPULATOR = "CMR"
    PERIPHERIES = "CPS"


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
    GRIPPER_GRASPING = {
        "TOP_FINGER": "UpArmServo",
        "LEFT_FINGER": "LeftArmServo",
        "RIGHT_FINGER": "RightArmServo",
    }
