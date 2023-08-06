from enum import Enum


class PlaneFlightModes(Enum):
    MANUAL = 0
    CIRCLE = 1
    STABILIZE = 2
    TRAINING = 3
    ACRO = 4
    FBWA = 5
    FBWB = 6
    CRUISE = 7
    AUTOTUNE = 8
    AUTO = 10
    RTL = 11
    LOITER = 12
    TAKEOFF = 13
    AVOID_ADSB = 14
    GUIDED = 15
    QSTABILIZE = 17
    QHOVER = 18
    QLOITER = 19
    QLAND = 20
    QRTL = 21
    QAUTOTUNE = 22
    QACRO = 23


class CopterFlightModes(Enum):
    STABILIZE = 0
    ACRO = 1
    ALT_HOLD = 2
    AUTO = 3
    GUIDED = 4
    LOITER = 5
    RTL = 6
    CIRCLE = 7
    LAND = 9
    DRIFT = 11
    FLIP = 14
    AUTOTUNE = 15
    POSHOLD = 16
    BRAKE = 17
    THROW = 18
    AVOID_ADSB = 19
    GUIDED_NOGPS = 20
    SMART_RTL = 21
    FLOWHOLD = 22
    ZIGZAG = 24


class MavMissionType(Enum):
    """
    Enumeration of MAVLink mission types.

    Values:
    - MAV_MISSION_TYPE_MISSION (int): Items are mission commands for the main mission.
    - MAV_MISSION_TYPE_FENCE (int): Specifies GeoFence area(s). Items are MAV_CMD_NAV_FENCE_ GeoFence items.
    - MAV_MISSION_TYPE_RALLY (int): Specifies the rally points for the vehicle. Rally points are alternative RTL points.
    - MAV_MISSION_TYPE_ALL (int): Only used in MISSION_CLEAR_ALL to clear all mission types.
    """

    MAV_MISSION_TYPE_MISSION = 0
    MAV_MISSION_TYPE_FENCE = 1
    MAV_MISSION_TYPE_RALLY = 2
    MAV_MISSION_TYPE_ALL = 255


class MavMissionResult(Enum):
    """
    Enumeration of mission results in a MISSION_ACK message.

    Values:
    - MAV_MISSION_ACCEPTED (int): Mission accepted OK.
    - MAV_MISSION_ERROR (int): Generic error / not accepting mission commands at all right now.
    - MAV_MISSION_UNSUPPORTED_FRAME (int): Coordinate frame is not supported.
    - MAV_MISSION_UNSUPPORTED (int): Command is not supported.
    - MAV_MISSION_NO_SPACE (int): Mission items exceed storage space.
    - MAV_MISSION_INVALID (int): One of the parameters has an invalid value.
    - MAV_MISSION_INVALID_PARAM1 (int): param1 has an invalid value.
    - MAV_MISSION_INVALID_PARAM2 (int): param2 has an invalid value.
    - MAV_MISSION_INVALID_PARAM3 (int): param3 has an invalid value.
    - MAV_MISSION_INVALID_PARAM4 (int): param4 has an invalid value.
    - MAV_MISSION_INVALID_PARAM5_X (int): x / param5 has an invalid value.
    - MAV_MISSION_INVALID_PARAM6_Y (int): y / param6 has an invalid value.
    - MAV_MISSION_INVALID_PARAM7 (int): z / param7 has an invalid value.
    - MAV_MISSION_INVALID_SEQUENCE (int): Mission item received out of sequence.
    - MAV_MISSION_DENIED (int): Not accepting any mission commands from this communication partner.
    - MAV_MISSION_OPERATION_CANCELLED (int): Current mission operation cancelled (e.g. mission upload, mission download).
    """

    MAV_MISSION_ACCEPTED = 0
    MAV_MISSION_ERROR = 1
    MAV_MISSION_UNSUPPORTED_FRAME = 2
    MAV_MISSION_UNSUPPORTED = 3
    MAV_MISSION_NO_SPACE = 4
    MAV_MISSION_INVALID = 5
    MAV_MISSION_INVALID_PARAM1 = 6
    MAV_MISSION_INVALID_PARAM2 = 7
    MAV_MISSION_INVALID_PARAM3 = 8
    MAV_MISSION_INVALID_PARAM4 = 9
    MAV_MISSION_INVALID_PARAM5_X = 10
    MAV_MISSION_INVALID_PARAM6_Y = 11
    MAV_MISSION_INVALID_PARAM7 = 12
    MAV_MISSION_INVALID_SEQUENCE = 13
    MAV_MISSION_DENIED = 14
    MAV_MISSION_OPERATION_CANCELLED = 15


class MavFrame(Enum):
    """
    Enumeration of coordinate frames used by MAVLink.

    Values:
    - MAV_FRAME_GLOBAL (int): Global (WGS84) coordinate frame + MSL altitude.
    - MAV_FRAME_LOCAL_NED (int): NED local tangent frame (x: North, y: East, z: Down) with origin fixed relative to earth.
    - MAV_FRAME_MISSION (int): NOT a coordinate frame, indicates a mission command.
    - MAV_FRAME_GLOBAL_RELATIVE_ALT (int): Global (WGS84) coordinate frame + altitude relative to the home position.
    - MAV_FRAME_LOCAL_ENU (int): ENU local tangent frame (x: East, y: North, z: Up) with origin fixed relative to earth.
    - MAV_FRAME_GLOBAL_INT (int): Global (WGS84) coordinate frame (scaled) + MSL altitude.
    - MAV_FRAME_GLOBAL_RELATIVE_ALT_INT (int): Global (WGS84) coordinate frame (scaled) + altitude relative to the home position.
    - MAV_FRAME_LOCAL_OFFSET_NED (int): NED local tangent frame (x: North, y: East, z: Down) with origin that travels with the vehicle.
    - MAV_FRAME_BODY_NED (int): DEPRECATED: Replaced by MAV_FRAME_BODY_FRD. Same as MAV_FRAME_LOCAL_NED when used to represent position values. Same as MAV_FRAME_BODY_FRD when used with velocity/acceleration values.
    - MAV_FRAME_BODY_OFFSET_NED (int): DEPRECATED: Replaced by MAV_FRAME_BODY_FRD. This is the same as MAV_FRAME_BODY_FRD.
    - MAV_FRAME_GLOBAL_TERRAIN_ALT (int): Global (WGS84) coordinate frame with AGL altitude (at the waypoint coordinate).
    - MAV_FRAME_GLOBAL_TERRAIN_ALT_INT (int): Global (WGS84) coordinate frame (scaled) with AGL altitude (at the waypoint coordinate).
    - MAV_FRAME_BODY_FRD (int): FRD local frame aligned to the vehicle's attitude (x: Forward, y: Right, z: Down) with an origin that travels with the vehicle.
    - MAV_FRAME_RESERVED_13 (int): DEPRECATED: Replaced by MAV_FRAME_BODY_FLU - Body fixed frame of reference, Z-up (x: Forward, y: Left, z: Up).
    - MAV_FRAME_RESERVED_14 (int): DEPRECATED: Replaced by MAV_FRAME_LOCAL_FRD - Odometry local coordinate frame of data given by a motion capture system, Z-down (x: North, y: East, z: Down).
    - MAV_FRAME_RESERVED_15 (int): DEPRECATED: Replaced by MAV_FRAME_LOCAL_FLU - Odometry local coordinate frame of data given by a motion capture system, Z-up (x: East, y: North, z: Up).
    - MAV_FRAME_RESERVED_16 (int): DEPRECATED: Replaced by MAV_FRAME_LOCAL_FRD - Odometry local coordinate frame of data given by a vision estimation system, Z-down (x: North, y: East, z: Down).
    - MAV_FRAME_RESERVED_17 (int): DEPRECATED: Replaced by MAV_FRAME_LOCAL_FLU - Odometry local coordinate frame of data given by a vision estimation system, Z-up (x: East, y: North, z: Up).
    - MAV_FRAME_RESERVED_18 (int): DEPRECATED: Replaced by MAV_FRAME_LOCAL_FRD - Odometry local coordinate frame of data given by an estimator running onboard the vehicle, Z-down (x: North, y: East, z: Down).
    - MAV_FRAME_RESERVED_19 (int): DEPRECATED: Replaced by MAV_FRAME_LOCAL_FLU - Odometry local coordinate frame of data given by an estimator running onboard the vehicle, Z-up (x: East, y: North, z: Up).
    - MAV_FRAME_LOCAL_FRD (int): FRD local tangent frame (x: Forward, y: Right, z: Down) with origin fixed relative to earth.
    - MAV_FRAME_LOCAL_FLU (int): FLU local tangent frame (x: Forward, y: Left, z: Up) with origin fixed relative to earth.
    """

    MAV_FRAME_GLOBAL = 0
    MAV_FRAME_LOCAL_NED = 1
    MAV_FRAME_MISSION = 2
    MAV_FRAME_GLOBAL_RELATIVE_ALT = 3
    MAV_FRAME_LOCAL_ENU = 4
    MAV_FRAME_GLOBAL_INT = 5
    MAV_FRAME_GLOBAL_RELATIVE_ALT_INT = 6
    MAV_FRAME_LOCAL_OFFSET_NED = 7
    MAV_FRAME_BODY_NED = 8
    MAV_FRAME_BODY_OFFSET_NED = 9
    MAV_FRAME_GLOBAL_TERRAIN_ALT = 10
    MAV_FRAME_GLOBAL_TERRAIN_ALT_INT = 11
    MAV_FRAME_BODY_FRD = 12
    MAV_FRAME_RESERVED_13 = 13
    MAV_FRAME_RESERVED_14 = 14
    MAV_FRAME_RESERVED_15 = 15
    MAV_FRAME_RESERVED_16 = 16
    MAV_FRAME_RESERVED_17 = 17
    MAV_FRAME_RESERVED_18 = 18
    MAV_FRAME_RESERVED_19 = 19
    MAV_FRAME_LOCAL_FRD = 20
    MAV_FRAME_LOCAL_FLU = 21
