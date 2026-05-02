from queue import Queue
from multiprocessing import Process, Event
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

class Beholder:
    def __init__(self, queue, shutdown_timeout=1.0):
        self._queue = queue
        self._exit_event = Event()
        self._proc = Process(target=self._run_task, args=(self._queue, self._exit_event), daemon=True)
        self._shutdown_timeout = shutdown_timeout

    def start(self):
        self._proc.start()

    def join(self):
        self._proc.join()

    def shutdown(self):
        self._exit_event.set()
        self._proc.join(self._shutdown_timeout)

        if self._proc.exitcode is None:
            self._proc.terminate()
            self._proc.join(self._shutdown_timeout)
        
        if self._proc.exitcode is None:
            self._proc.kill()

    @staticmethod
    def _run_task(queue: Queue, exit_event: Event):
        app = QtWidgets.QApplication([])

        win = pg.plot(title='Beholder')
        win.addLegend()

        data = {}
        curves = {}
        refresh = {}

        while not exit_event.is_set():
            while not exit_event.is_set() and not queue.empty():
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

        app.quit()