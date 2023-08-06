import logging
from typing import Optional, Union

from pymavlink.dialects.v20.ardupilotmega import (
    MAV_CMD_COMPONENT_ARM_DISARM,
    MAV_CMD_DO_REPOSITION,
    MAV_CMD_DO_SET_MODE,
    MAV_CMD_DO_SET_SERVO,
    MAV_CMD_NAV_RETURN_TO_LAUNCH,
    MAV_CMD_NAV_WAYPOINT,
    MAVLink,
)

from .commands import (
    get_command_int_message,
    get_command_long_message,
    get_mission_count_message,
    get_mission_item_int,
)
from .enums import CopterFlightModes, PlaneFlightModes
from .telemetry_source import TelemetrySource

logger = logging.getLogger(__name__)

MY_SRC_ID = 1
MY_CMP_ID = 191


class UAV:
    def __init__(self, target_system: int = 1, target_component: int = 1) -> None:
        self.target_system = target_system
        self.target_component = target_component
        self.mav = MAVLink(0, MY_SRC_ID, MY_CMP_ID)

        self.telem_source = TelemetrySource()
        self.telem_source.make_direct_connection()

    def arm(self) -> None:
        """
        Arms motors.
        """
        msg = get_command_long_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_COMPONENT_ARM_DISARM,
            param1=1,
        )

        self.telem_source.send(msg.pack(self.mav))
        logger.info("Arm command sent.")

    def disarm(self) -> None:
        """
        Disarms motors.
        """
        msg = get_command_long_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_COMPONENT_ARM_DISARM,
            param1=0,
        )

        self.telem_source.send(msg.pack(self.mav))
        logger.info("Disarm command sent.")

    def set_mode(self, mode: Union[PlaneFlightModes, CopterFlightModes]) -> None:
        """
        Set system mode.

        Args:
        - mode: ardupilot flight mode you want to set.
        """
        msg = get_command_long_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_DO_SET_MODE,
            param1=1,
            param2=mode.value,
        )

        self.telem_source.send(msg.pack(self.mav))
        logger.info("Set mode command sent")

    def set_servo(self, instance_number: int, pwm: int) -> None:
        """
        Set a servo to a desired PWM value.

        Args:
        - instance_number: servo number.
        - pwm: PWM to set.
        """
        msg = get_command_long_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_DO_SET_SERVO,
            param1=instance_number,
            param2=pwm,
        )

        self.telem_source.send(msg.pack(self.mav))
        logger.info("Set servo command sent.")

    def flight_to_gps_position(self, lat_int: int, lon_int: int, alt_m: float) -> None:
        """
        Works only in Guided mode. Reposition the vehicle to a specific WGS84 global position.
        """
        msg = get_command_int_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_DO_REPOSITION,
            x=lat_int,
            y=lon_int,
            z=alt_m,
        )

        self.telem_source.send(msg.pack(self.mav))
        logger.info("Flight to point command sent.")

    def send_mission_count(self, mission_elements_count: int) -> None:
        """
        Send the number of items in a mission. This is used to initiate mission upload.

        Args:
        - mission_elements_count (int): Number of mission items in the sequence.
        """
        msg = get_mission_count_message(
            target_system=self.target_system,
            target_component=self.target_component,
            count=mission_elements_count,
        )

        self.telem_source.send(msg.pack(self.mav))
        logger.info("mission_count message sent.")

    def send_mission_waypoint_item(
        self,
        seq: int,
        lat_int: int,
        lon_int: int,
        alt_m: float,
        accept_radius_m: float,
        hold_time_s: float = 0,
        pass_radius_m: float = 0,
        yaw_deg: Optional[float] = None,
    ) -> None:
        """
        Sends a mission waypoint to navigate to.

        Args:
        - seq (int): Waypoint ID (sequence number). Starts at zero. Increases monotonically for each mission item.
        - lat (int): Latitude of the waypoint.
        - lon (int): Longitude of the waypoint.
        - alt_m (float): Altitude of the waypoint in meters.
        - accept_radius_m (float): Acceptance radius. If the sphere with this radius is hit, the waypoint counts as reached.
        - hold_time_s (float, optional): Hold time at the waypoint in seconds. Ignored by fixed-wing vehicles. Defaults to 0.
        - pass_radius_m (float, optional): Pass radius. If > 0, it specifies the radius to pass by the waypoint.
            Allows trajectory control. Positive value for clockwise orbit, negative value for counterclockwise orbit. Defaults to 0.
        - yaw_deg (float, optional): Desired yaw angle at the waypoint for rotary-wing vehicles.
            Set to NaN to use the current system yaw heading mode. Defaults to None.

        Returns: None
        """
        msg = get_mission_item_int(
            target_system=self.target_system,
            target_component=self.target_component,
            seq=seq,
            command=MAV_CMD_NAV_WAYPOINT,
            param1=hold_time_s,
            param2=accept_radius_m,
            param3=pass_radius_m,
            param4=yaw_deg,
            x=lat_int,
            y=lon_int,
            z=alt_m,
        )

        self.telem_source.send(msg.pack(self.mav))
        logger.info("mission_waypoint message sent.")

    def send_mission_rtl_item(
        self,
        seq: int,
    ) -> None:
        """
        Sends a mission return to launch location.

        Args:
        - seq (int): Waypoint ID (sequence number). Starts at zero. Increases monotonically for each mission item.

        Returns: None
        """
        msg = get_mission_item_int(
            target_system=self.target_system,
            target_component=self.target_component,
            seq=seq,
            command=MAV_CMD_NAV_RETURN_TO_LAUNCH,
        )

        self.telem_source.send(msg.pack(self.mav))
        logger.info("mission_rtl message sent.")
