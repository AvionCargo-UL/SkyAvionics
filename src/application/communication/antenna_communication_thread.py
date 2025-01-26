import threading
import time
from queue import Queue


class AntennaCommunicationThread(threading.Thread):
    def __init__(self, refresh_rate_s: float, send_queue: Queue, response_queue: Queue):
        threading.Thread.__init__(self)

        self.__refresh_rate_s: float = refresh_rate_s
        self.__send_queue: Queue = send_queue
        self.__response_queue: Queue = response_queue

        self.__stop_event = threading.Event()

    def run(self):
        while not self.__stop_event.is_set():

            # TODO : Parse DATA from GCS
            # TODO : Send DATA to GCS
            
            time.sleep(self.__thread_frequency_second)

    def stop(self):
        self.__stop_event.set()
