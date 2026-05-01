from multiprocessing import Process, Queue
from concurrent.futures import ProcessPoolExecutor
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from typing import NamedTuple

from time import sleep
import random

class DataPoint(NamedTuple):
    key: str
    value: float

class Beholder:
    def __init__(self, queue, proc):
        self._queue = queue
        self._proc = proc

    @staticmethod
    def _run_task(queue: Queue):
        app = QtWidgets.QApplication([])
        win = pg.plot(title='Beholder')
        win.addLegend()

        data = {}
        curves = {}
        refresh = {}

        while True:
            while not queue.empty():
                key, value = queue.get()

                if key not in data:
                    data[key] = []
                    curves[key] = win.plot(name=key, pen=pg.intColor(len(curves)))
                    
                data[key].append(value)
                refresh[key] = True

            for key, value in data.items():
                if refresh[key] == False:
                    continue

                curves[key].setData(data[key])

            app.processEvents()

    @classmethod
    def spawn(cls):
        queue = Queue()
        proc = Process(target=cls._run_task, args=(queue,), daemon=True)
        proc.start()

        return Beholder(queue, proc)

    @property
    def queue(self):
        return self._queue

    @property
    def proc(self):
        return self._proc

    def send(self, key, value):
        self.queue.put((key, value))

class GlobalQueue:
    @classmethod
    def attach_queue(cls, queue):
        cls._queue = queue

    @classmethod
    def send(cls, key, value):
        cls._queue.put((key, value))

def worker(key):
    while True:
        GlobalQueue.send(key, random.randint(20,30))
        sleep(.01)

if __name__ == '__main__':
    bh = Beholder.spawn()

    with ProcessPoolExecutor(initializer=GlobalQueue.attach_queue, initargs=(bh.queue,)) as executor:
        futures = [executor.submit(worker, key) for key in ['aa', 'bb']]

        while True:
            bh.send('a', random.randint(-10,10))
            bh.send('b', random.randint(-10,10))
            sleep(.01)