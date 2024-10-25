from typing import List

import cv2

from pymavlink import mavutil
from pymavlink.dialects.v10.ASLUAV import MAVLink_mission_item_message

from src.configuration.environment.context.development_context import DevelopmentContext


def test_pymavlink():
    print("Connecting...")
    # master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
    master = mavutil.mavlink_connection("COM5", 115200)
    print("Connected!")

    master.wait_heartbeat()

    mission_items: List[MAVLink_mission_item_message] = [
        master.mav.mission_item_encode(
            0,
            0,
            0,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            10,
        ),  # Takeoff
        master.mav.mission_item_encode(
            0,
            0,
            1,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            0,
            0,
            0,
            0,
            0,
            37.874,
            -122.259,
            10,
        ),  # Waypoint 1
        master.mav.mission_item_encode(
            0,
            0,
            2,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            0,
            0,
            0,
            0,
            0,
            37.874,
            -122.5,
            20,
        ),  # Waypoint 2
        master.mav.mission_item_encode(
            0,
            0,
            3,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            0,
            0,
            0,
            0,
            0,
            37.8,
            -122.259,
            20,
        ),  # Waypoint 3
        master.mav.mission_item_encode(
            0,
            0,
            4,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ),  # Return to launch
    ]

    print("Sending!")

    master.mav.mission_count_send(0, 0, len(mission_items))

    for i, item in enumerate(mission_items):
        item: MAVLink_mission_item_message
        master.mav.mission_item_send(
            target_system=item.target_system,
            target_component=item.target_component,
            seq=i,
            frame=item.frame,
            command=item.command,
            current=0 if i > 0 else 1,
            autocontinue=item.autocontinue,
            param1=item.param1,
            param2=item.param2,
            param3=item.param3,
            param4=item.param4,
            x=item.x,
            y=item.y,
            z=item.x,
        )

    print("Mission uploaded.")


def main():

    application_context = DevelopmentContext()
    application_context.build_application()

    try:
        application_context.start_application()
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    # test_pymavlink()
