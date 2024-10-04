import cv2

from src.domain.vision.exception.unable_to_read_frame_exception import (
    UnableToReadFrameException,
)
from src.domain.vision.vision_thread import VisionThread


def main():
    vision_thread = VisionThread()
    vision_thread.start()

    try:
        while vision_thread.is_alive():
            pass
    except UnableToReadFrameException as e:
        vision_thread.dispose()
        print(e)
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
