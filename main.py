from typing import List

import cv2

from src.domain.vision.aruco import Aruco
from src.domain.vision.vision_controller import VisionController


def main():
    vision_controller = VisionController()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        arucos: List[Aruco] = vision_controller.do_aruco_detection(frame)
        if len(arucos) > 0:
            print(arucos)

        # if ids is not None:
        #     # Draw detected markers on the frame
        #     cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        cv2.imshow('Webcam with ArUco Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
