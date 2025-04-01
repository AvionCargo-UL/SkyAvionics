import threading
import uvicorn
from queue import Queue
from fastapi import FastAPI

from src.interfaces.api.video_routes import create_video_router


class FastAPIThread(threading.Thread):
    def __init__(
        self,
        send_frame_queue: Queue,
        send_telemetry_queue: Queue = None,
        response_queue: Queue = None,
    ):
        threading.Thread.__init__(self)
        self.__stop_event = threading.Event()

        # Create the FastAPI app
        self.app = FastAPI()

        # Include the video router
        self.app.include_router(create_video_router(send_frame_queue))

        # Store queues for potential future use
        self.send_frame_queue = send_frame_queue
        self.send_telemetry_queue = send_telemetry_queue
        self.response_queue = response_queue

    def run(self):
        # Run Uvicorn server with 'app' in a way that can be stopped
        config = uvicorn.Config(self.app, host="0.0.0.0", port=8000, log_level="info")
        self.server = uvicorn.Server(config)
        self.server.run()

    def stop(self):
        self.__stop_event.set()
        # Properly shutdown the server when available
        if hasattr(self, "server"):
            self.server.should_exit = True
