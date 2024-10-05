import cv2

from src.domain.vision.exception.unable_to_read_frame_exception import (
    UnableToReadFrameException,
)
from src.domain.vision.vision_thread import VisionThread


def main():
    vision_thread = VisionThread()
    vision_thread.start()

    try:
        vision_thread.join()
    except UnableToReadFrameException as e:
        print(e)
    finally:
        vision_thread.dispose()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
