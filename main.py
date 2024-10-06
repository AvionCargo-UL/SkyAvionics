import cv2

from src.configuration.environment.context.development_context import DevelopmentContext


def main():

    application_context = DevelopmentContext()
    application_context.build_application()

    try:
        application_context.start_application()
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
