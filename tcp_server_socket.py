import socket
import sys
from common import *
import pickle
import zlib
from concurrent.futures import ThreadPoolExecutor
import logging
import threading
import struct


logger = logging.getLogger('tcp_server')


def do_recv(csock, host, port):
    count = 0
    data = b""
    payload_size = struct.calcsize(">L")
    logger.debug("payload_size: %d" % payload_size)
    while True:
        try:
            while len(data) < payload_size:
                data += csock.recv(config['recv_buf_size'])
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += csock.recv(config['recv_buf_size'])
            recv_bytes = data[:msg_size]
            data = data[msg_size:]
            detections = pickle.loads(recv_bytes, fix_imports=True, encoding="bytes")
            print('receive ====>\n', detections)
            count += 1
            logger.info(
                '+%d Received %d bytes data from %s:%d' % (count, len(recv_bytes), host, port))
        except KeyboardInterrupt:
            logger.error('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.error('Exception: %s' % e)
            break

    logger.info('Close socket for client(%s:%d).' % (host, port))
    csock.close()


def do_accept(ssock):
    pool = ThreadPoolExecutor(config['thread_pool_max_workers'])
    while True:
        try:
            (csock, (host, port)) = ssock.accept()
            logger.info('Accept from %s:%d' % (host, port))
            pool.submit(do_recv, csock, host, port)
        except KeyboardInterrupt:
            logger.error('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.error('Exception: %s' % e)
            break

    logger.info('Close server socket~~~')
    ssock.close()
        
        
if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info('TCP socket created successfully...')
    except OSError as os_err:
        logger.error('Create socket, OSError: %s' % os_err)
        sys.exit(1)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse socket
    sock.bind((config['host'], config['port']))
    logger.info('TCP socket bind at %s:%d successfully...' % (config['host'], config['port']))
    sock.listen(config['queue_size_for_listen'])
    t = threading.Thread(target=do_accept, args=(sock,))
    t.start()
