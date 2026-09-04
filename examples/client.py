from time import sleep
import random
import argparse

from beholder import QueueManager

# python client.py -a 127.0.0.1 -p 5555 -k 123

if __name__=='__main__':
    parser = argparse.ArgumentParser('Beholder client')
    parser.add_argument('-a', '--address', help='queue manager address', type=str, default='127.0.0.1')
    parser.add_argument('-p', '--port', help='queue manager port', type=int, default=5555)
    parser.add_argument('-k', '--authkey', help='queue manager authentication key', type=lambda x: x.encode(), default=b'')

    args = parser.parse_args()

    QueueManager.connect_global((args.address, args.port), args.authkey)

    while True:
        QueueManager.get_global_queue().put(('xyz', random.randint(-30,20)))
        sleep(0.1)