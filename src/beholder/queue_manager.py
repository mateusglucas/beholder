from multiprocessing.managers import BaseManager
from queue import Queue

class QueueManager(BaseManager):
    _queue = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register('get_queue', callable=self._get_queue)

    def _get_queue(self):
        if self._queue is None:
            self._queue = Queue()

        return self._queue

    @classmethod
    def connect_global(cls, *args, **kwargs):
        cls._global_queue_manager = QueueManager(*args, **kwargs)
        cls._global_queue_manager.connect()
        
        cls._global_queue = cls._global_queue_manager.get_queue()

    @classmethod
    def get_global_queue(cls):
        return cls._global_queue