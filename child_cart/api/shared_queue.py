import queue
import threading

class SharedQueueSingleton:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.queue = queue.Queue()
        return cls._instance

    def put(self, item):
        with self._instance_lock:
            self.queue.put(item)

    def get(self):
        with self._instance_lock:
            return self.queue.get()

    def empty(self):
        with self._instance_lock:
            return self.queue.empty()
