from typing import Optional

from pymavlink.dialects.v20.ardupilotmega import (
    MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
    MAVLink_command_int_message,
    MAVLink_command_long_message,
    MAVLink_mission_count_message,
    MAVLink_mission_item_int_message,
)

from .enums import MavFrame, MavMissionType


def get_command_long_message(
    target_system: int,
    target_component: int,
    command: int,
    confirmation: int = 0,
    param1: float = 0,
    param2: float = 0,
    param3: float = 0,
    param4: float = 0,
    param5: float = 0,
    param6: float = 0,
    param7: float = 0,
) -> MAVLink_command_long_message:
    """MAVLink command long message wraper

    Args:
    - target_system (int): message target system id
    - target_component (int): message target component id
    - command (int): command number
    - confirmation (int, optional): Defaults to 0.
    - param1 (float, optional): Defaults to 0.
    - param2 (float, optional): Defaults to 0.
    - param3 (float, optional): Defaults to 0.
    - param4 (float, optional): Defaults to 0.
    - param5 (float, optional): Defaults to 0.
    - param6 (float, optional): Defaults to 0.
    - param7 (float, optional): Defaults to 0.

    Returns: MAVLink_command_long_message: message object
    """
    return MAVLink_command_long_message(
        target_system,
        target_component,
        command,
        confirmation,
        param1,
        param2,
        param3,
        param4,
        param5,
        param6,
        param7,
    )


def get_command_int_message(
    target_system: int,
    target_component: int,
    command: int,
    x: int,  # pylint: disable=invalid-name
    y: int,  # pylint: disable=invalid-name
    z: float,  # pylint: disable=invalid-name
    frame: int = MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
    current: int = 0,
    autocontinue: int = 0,
    param1: float = 0,
    param2: float = 0,
    param3: float = 0,
    param4: float = 0,
) -> MAVLink_command_int_message:
    """MAVLink command int message wraper

    Args:
    - target_system (int): message target system id
    - target_component (int): message target component id
    - command (int): command number
    - x (int): local: x position in meters * 1e4, global: latitude in degrees * 10^7
    - y (int): local: y position in meters * 1e4, global: longitude in degrees * 10^7
    - z (float): z position: global: altitude in meters (relative or absolute, depending on frame).
    - frame (int): The coordinate system of the COMMAND. Defaults MAV_FRAME_GLOBAL_RELATIVE_ALT_INT.
    - current (int): Not used.
    - autocontinue: (int): Not used.
    - param1: (float, optional): Defaults to 0.
    - param2: (float, optional): Defaults to 0.
    - param3: (float, optional): Defaults to 0.
    - param4: (float, optional): Defaults to 0.

    Returns: MAVLink_command_int_message: message object
    """
    return MAVLink_command_int_message(
        target_system,
        target_component,
        frame,
        command,
        current,
        autocontinue,
        param1,
        param2,
        param3,
        param4,
        x,
        y,
        z,
    )


def get_mission_count_message(
    target_system: int,
    target_component: int,
    count: int,
    mission_type: MavMissionType = MavMissionType.MAV_MISSION_TYPE_MISSION,
) -> MAVLink_mission_count_message:
    """MAVLink mission count message wraper

    Args:
    - target_system (int): message target system id
    - target_component (int): message target component id
    - count (int): Number of mission items in the sequence
    - mission_type (MavMissionType): Mission type

    Returns: MAVLink_mission_count_message: message object
    """
    return MAVLink_mission_count_message(
        target_system, target_component, count, mission_type.value
    )


def get_mission_item_int(
    target_system: int,
    target_component: int,
    seq: int,
    command: int,
    param1: float = 0,
    param2: float = 0,
    param3: float = 0,
    param4: Optional[float] = 0,
    x: int = 0,
    y: int = 0,
    z: float = 0,
    current: int = 0,
    autocontinue: int = 1,
    frame: MavFrame = MavFrame.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
    mission_type: MavMissionType = MavMissionType.MAV_MISSION_TYPE_MISSION,
) -> MAVLink_mission_item_int_message:
    """MAVLink mission item int message wraper

    Args:
    - target_system (int): System ID.
    - target_component (int): Component ID.
    - seq (int): Waypoint ID (sequence number). Starts at zero. Increases monotonically for each waypoint, no gaps in the sequence (0, 1, 2, 3, 4).
    - frame (MavFrame): The coordinate system of the waypoint (MAV_FRAME).
    - command (int): The scheduled action for the waypoint (MAV_CMD).
    - current (int): Indicates if this waypoint is the current one in the mission (false: 0, true: 1).
    - autocontinue (int): Indicates whether to autocontinue to the next waypoint (0: false, 1: true). Set false to pause the mission after the item completes.
    - param1 (float): PARAM1, see MAV_CMD enum.
    - param2 (float): PARAM2, see MAV_CMD enum.
    - param3 (float): PARAM3, see MAV_CMD enum.
    - param4 (float): PARAM4, see MAV_CMD enum.
    - x (int): PARAM5 / local: x position in meters * 1e4, global: latitude in degrees * 10^7.
    - y (int): PARAM6 / y position: local: x position in meters * 1e4, global: longitude in degrees * 10^7.
    - z (float): PARAM7 / z position: global: altitude in meters (relative or absolute, depending on the frame).
    - mission_type (int): Mission type (MAV_MISSION_TYPE).

    Returns: MAVLink_command_int_message: message object
    """
    return MAVLink_mission_item_int_message(
        target_system,
        target_component,
        seq,
        frame.value,
        command,
        current,
        autocontinue,
        param1,
        param2,
        param3,
        param4,
        x,
        y,
        z,
        mission_type,
    )
