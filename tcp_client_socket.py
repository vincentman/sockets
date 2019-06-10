import socket
import sys
from common import *
import pickle
import zlib
import struct

detections = [{"name": "name1", "age": 18, "gender": "male"}, {"name": "name2", "age": 20, "gender": "female"}]


if __name__ == '__main__':
    logger = logging.getLogger('tcp_client')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        logger.info('TCP socket created successfully...')
    except OSError as os_err:
        logger.error('Create socket, OSError: %s' % os_err)
        sys.exit(1)

    try:
        sock.connect((config['to_server_host'], config['to_server_port']))
        logger.info(
            'TCP socket connect at %s:%d successfully...' % (config['to_server_host'], config['to_server_port']))
    except OSError as os_err:
        logger.error('Connect socket, OSError: %s' % os_err)
        sys.exit(1)

    while True:
        try:
            send_bytes = pickle.dumps(detections)
            logger.info('Send %d bytes data...' % len(send_bytes))
            sock.sendall(struct.pack(">L", len(send_bytes)) + send_bytes)
        except KeyboardInterrupt:
            logger.error('KeyboardInterrupt~~~')
            logger.info('Close socket~~~')
            sock.close()
        except (BrokenPipeError, ConnectionResetError, socket.timeout) as e:
            logger.error('Error: %s' % e)
            logger.info('Close socket and create socket again~~~')
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            logger.info('TCP socket created successfully...')
            reconnect = 1
            while reconnect <= 60:
                try:
                    logger.info('Try to reconnect to server...%d' %reconnect)
                    sock.connect((config['to_server_host'], config['to_server_port']))
                    logger.info('TCP socket connect at %s:%d successfully...' % (
                        config['to_server_host'], config['to_server_port']))
                    break
                except OSError as os_err:
                    logger.error('Connect socket, OSError: %s' % os_err)
                    reconnect += 1
                    time.sleep(1)
            if reconnect > 60:
                logger.info('Reconnect failed! Close socket~~~')
                sock.close()
        except Exception as e:
            logger.error('Exception: %s' % e)
            logger.info('Close socket~~~')
            sock.close()

    logger.info('Close socket~~~')
    sock.close()
