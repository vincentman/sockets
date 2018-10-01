import socket
import sys
from common import *
import pickle
import zlib
import logging


if __name__ == '__main__':
    logger = logging.getLogger('udp_server')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logger.info('UDP socket created successfully...')
    except OSError as os_err:
        logger.error('Create socket, OSError: %s' % os_err)
        sys.exit(1)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse socket
    sock.bind((config['host'], config['port']))

    while True:
        try:
            data, (host, port) = sock.recvfrom(config['recv_buf_size'])
            if not data:
                print('No data received...')
            else:
                logger.info('Received %d bytes data from %s:%d' % (len(data), host, port))
                data = zlib.decompress(data)
                detections = pickle.loads(data)
                logger.debug('Data...%s' % detections)
        except KeyboardInterrupt:
            logger.error('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.error('Exception: %s' % e)
            break

    logger.info('Close socket~~~')
    sock.close()
