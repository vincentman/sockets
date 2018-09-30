import socket
import sys
from common import *
import pickle
import zlib
import logging


if __name__ == '__main__':
    log_type = 'udp_server'
    logger = logging.getLogger(log_type)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    log_file_name = '%s_%s.log' % (log_type, time.strftime("%Y-%m-%d", time.localtime()))
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M',
                        handlers=[logging.FileHandler(log_file_name, 'a', 'utf-8'), console])


    config = load_config()
    print('config =>', config)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logger.debug('UDP socket created successfully...')
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
            logger.info('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.info('Exception: %s' % e)
            break

    logger.info('Close socket~~~')
    sock.close()
