import threading

from log import log


class TestThread:
    def __init__(self):
        self.wait_interval = 0.5
        self.worker_thread = None
        self.thread_lock = threading.Lock()
        self.stop_event = threading.Event()

    def __worker(self):
        log.info("TestThread.__worker() is running...")
        while not self.stop_event.is_set():
            with self.thread_lock:
                pass
            self.stop_event.wait(self.wait_interval)

    def start(self):
        self.worker_thread = threading.Thread(target=self.__worker,name="TestThread")
        self.worker_thread.start()

    def stop(self):
        self.stop_event.set()
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join()
        self.worker_thread = None