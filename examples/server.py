import argparse

from beholder.queue_manager import QueueManager
from beholder.beholder import Beholder

# python server.py -a 127.0.0.1 -p 5555 -k 123

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Beholder server')
    parser.add_argument('-a', '--address', help='queue manager address', type=str, default='127.0.0.1')
    parser.add_argument('-p', '--port', help='queue manager port', type=int, default=5555)
    parser.add_argument('-k', '--authkey', help='queue manager authentication key', type=lambda x: x.encode(), default=b'')

    args = parser.parse_args()

    address = (args.address, args.port)
    authkey = args.authkey

    manager = QueueManager(address, authkey)
    manager.start()

    queue = manager.get_queue()

    bh = Beholder(queue)
    bh.start()

    bh.join()
    manager.join()