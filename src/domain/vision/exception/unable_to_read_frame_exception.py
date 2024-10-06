class UnableToReadFrameException(RuntimeError):

    MESSAGE: str = "Unable to read frame from camera index %s"

    def __init__(self, camera_index: int):
        super().__init__(self.MESSAGE % camera_index)
