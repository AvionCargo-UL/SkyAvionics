from typing import List

from pymavlink import mavutil
from pymavlink.mavutil import mavserial

from src.domain.mavlink.mavlink_mission_item import MavlinkMissionItem


class MavlinkService:
    def __init__(self, port: str, baudrate: int, timeout_ms: int, retries: int):
        self.__mavlink_server: mavserial = mavutil.mavlink_connection(port, baudrate)

        for i in range(retries):
            print(f"Connecting to mavlink {i+1}/{retries}")
            try:
                self.__mavlink_server.wait_heartbeat(timeout=timeout_ms)
                print("Connection established!")
                break
            except TimeoutError:
                if i == retries - 1:
                    print("Max retries reached. Unable to connect to mavlink.")
                else:
                    print("Timeout! Unable to connect to mavlink... retrying.")

    def upload_mission(self, mission_items: List[MavlinkMissionItem]):
        self.__mavlink_server.waypoint_clear_all_send()

        self.__mavlink_server.mav.command_long_send(
            1,  # Target system
            1,  # Target component
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Command
            0,  # Confirmation
            1,  # Arm (0 to disarm)
            0,
            0,
            0,
            0,
            0,
            0,  # Unused parameters
        )
        response = self.__mavlink_server.recv_match(type="COMMAND_ACK", blocking=True)
        if response:
            print(f"Received ACK ARM: {response}")
        else:
            print("No response received.")

        guided = self.__mavlink_server.mode_mapping()["AUTO"]
        self.__mavlink_server.mav.command_long_send(
            1,  # Target system
            1,  # Target component
            mavutil.mavlink.MAV_CMD_DO_SET_MODE,  # Command
            0,  # Confirmation
            guided,  # Arm (0 to disarm)
            0,
            0,
            0,
            0,
            0,
            0,  # Unused parameters
        )
        print(guided)
        response = self.__mavlink_server.recv_match(type="COMMAND_ACK", blocking=True)
        if response:
            print(f"Received ACK GUIDED: {response}")
        else:
            print("No response received.")

        self.__mavlink_server.mav.mission_count_send(0, 0, len(mission_items))

        for item in mission_items:
            self.__mavlink_server.mav.mission_item_send(**item.to_dict())

        print("Mission uploaded!")
