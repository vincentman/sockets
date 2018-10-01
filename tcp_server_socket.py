import socket
import sys
from common import *
import pickle
import zlib
from concurrent.futures import ThreadPoolExecutor
import logging


def do_recv(csock, host, port):
    count = 0
    while True:
        try:
            data = csock.recv(config['recv_buf_size'])
            if not data:
                logger.info('Received 0 bytes data from %s:%d.' % (host, port))
                break
            else:
                count += 1
                logger.info('+%d Received %d bytes data from %s:%d' % (count, len(data), host, port))
                data = zlib.decompress(data)
                detections = pickle.loads(data)
                logger.debug('Data...%s' % detections)
        except KeyboardInterrupt:
            logger.error('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.error('Exception: %s' % e)
            break

    logger.info('Close socket for client(%s:%d).' % (host, port))
    csock.close()


if __name__ == '__main__':
    logger = logging.getLogger('tcp_server')
    pool = ThreadPoolExecutor(config['thread_pool_max_workers'])

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info('TCP socket created successfully...')
    except OSError as os_err:
        logger.error('Create socket, OSError: %s' % os_err)
        sys.exit(1)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse socket
    sock.bind((config['host'], config['port']))
    sock.listen(config['queue_size_for_listen'])

    while True:
        try:
            (csock, (host, port)) = sock.accept()
            logger.info('Accept from %s:%d' % (host, port))
            pool.submit(do_recv, csock, host, port)
        except KeyboardInterrupt:
            logger.error('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.error('Exception: %s' % e)
            break

    logger.info('Close server socket~~~')
    sock.close()
