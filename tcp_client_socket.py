import socket
import sys
from common import *
import pickle
import zlib

detections = [{"name": "name1", "age": 18, "gender": "male"}, {"name": "name2", "age": 20, "gender": "female"}]


if __name__ == '__main__':
    logger = logging.getLogger('tcp_client')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info('TCP socket created successfully...')
    except OSError as os_err:
        logger.error('Create socket, OSError: %s' % os_err)
        sys.exit(1)

    try:
        sock.connect((config['host'], config['port']))
    except OSError as os_err:
        logger.error('Connect socket, OSError: %s' % os_err)
        sys.exit(1)

    while True:
        try:
            data = pickle.dumps(detections)
            data = zlib.compress(data)
            if len(data) > config['recv_buf_size']:
                logger.warning('Data exceeds buffer size of server. Drop data!!')
                time.sleep(1)
                continue
            logger.info('Send %d bytes data...' % len(data))
            logger.debug('Data...%s' % detections)
            sent_bytes = sock.send(data)
            logger.info('%d bytes data sent...' % sent_bytes)
            if len(data) != sent_bytes:
                logger.warning('Not all data sent completely!!')
            time.sleep(1)
        except KeyboardInterrupt as key_interrupt:
            logger.error('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.error('Exception: %s' % e)
            break

    logger.info('Close socket~~~')
    sock.close()
