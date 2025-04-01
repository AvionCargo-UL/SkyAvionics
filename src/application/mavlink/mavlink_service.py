from typing import List
import threading
import time

from pymavlink import mavutil
from pymavlink.mavutil import mavserial

from serial.serialutil import SerialException

from src.domain.mavlink.mavlink_mission_item import MavlinkMissionItem
from src.domain.mavlink.mavlink_telemetry import MavlinkTelemetry


class MavlinkThread(threading.Thread):
    def __init__(self, device: str, baudrate: int, timeout_ms: int, retries: int, refresh_rate_s : float):
        threading.Thread.__init__(self)
        self.__mavlink_server: mavserial
        self.__refresh_rate_s = refresh_rate_s
        self.__stop_event = threading.Event()
        self.telemetry_data = None
        self.connection_secured = False

        try:
            self.__mavlink_server: mavserial = mavutil.mavlink_connection(device = device, 
                                                                          baud = baudrate,
                                                                          rettries = retries,
                                                                          timeout = timeout_ms)
            self.__mavlink_server.wait_heartbeat(timeout=timeout_ms)

        except SerialException as e:
            print(f"\n\nSERIAL CONNECTION FAILED:\n{e}\n\nKILLED MAVLINK THREAD\n\n")
            self.__stop_event.set()

    def download_telemetry(self):
        msg = self.__mavlink_server.recv_match(
            type="GLOBAL_POSITION_INT", blocking=True
        )
        hb_msg = self.__mavlink_server.recv_match(type="HEARTBEAT", blocking=True)
        battery_msg = self.__mavlink_server.recv_match(type="SYS_STATUS", blocking=True)

        return MavlinkTelemetry(
            time_boot_ms=msg.time_boot_ms if msg else 0,
            lat=msg.lat / 1e7 if msg else 0.0,
            lon=msg.lon / 1e7 if msg else 0.0,
            alt=msg.alt / 1000 if msg else 0.0,
            relative_alt=msg.relative_alt / 1000 if msg else 0.0,
            vx=msg.vx / 100 if msg else 0.0,
            vy=msg.vy / 100 if msg else 0.0,
            vz=msg.vz / 100 if msg else 0.0,
            heading=msg.hdg / 100 if msg else 0.0,
            airspeed=0.0,  # Requires different message type
            groundspeed=0.0,  # Requires different message type
            throttle=0.0,  # Requires different message type
            battery_voltage=battery_msg.voltage_battery / 1000 if battery_msg else 0.0,
            battery_current=battery_msg.current_battery / 100 if battery_msg else 0.0,
            battery_remaining=battery_msg.battery_remaining if battery_msg else 0.0,
            gps_num_satellites=hb_msg.satellites_visible if hb_msg else 0,
            gps_fix_type=hb_msg.fix_type if hb_msg else 0,
            armed=(
                (hb_msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED) != 0
                if hb_msg
                else False
            ),
        )

    def run(self):
        while not self.__stop_event.is_set():
            if self.connection_secured:
                self.telemetry_data = self.download_telemetry()
                print(self.telemetry_data.to_dict())
            time.sleep(self.__refresh_rate_s)

    def stop(self):
        self.__stop_event.set()

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

    def adjust_mission(self):
        # TODO : Parse the information from the vision and the GPS, and update mission item
        pass
