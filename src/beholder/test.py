from time import sleep
import random

from queue_manager import QueueManager

if __name__=='__main__':
    QueueManager.connect_global(('127.0.0.1', 5555), b'')

    while True:
        QueueManager.get_global_queue().put(('xyz', random.randint(-30,20)))
        sleep(0.1)