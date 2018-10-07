import socket
import sys
from common import *
import pickle
import zlib

detections = [{"name": "name1", "age": 18, "gender": "male"}, {"name": "name2", "age": 20, "gender": "female"}]


def send(sock, data):
    logger.info('UDP socket, send %d bytes data...' % len(data))
    sent_bytes = sock.sendto(data, (config['host'], config['port']))
    logger.info('UDP socket, %d bytes data sent...' % sent_bytes)
    if len(data) != sent_bytes:
        logger.warning('Not all data sent completely!!')
    time.sleep(1)


def get_send_bytes(header, payload):
    bs = bytearray()
    bs.append(header)
    bs.extend(payload)
    return bs


def fragment_data(data):
    payload_size = config['recv_buf_size'] - 1
    if len(data) <= payload_size:
        logger.info('Data have only one part, payload size:%d' % len(data))
        send(sock, get_send_bytes(0x02, data))
    else:
        if len(data) % payload_size == 0:
            chunks = len(data) // payload_size
        else:
            chunks = len(data) // payload_size + 1
        for i in range(chunks - 1):
            part = data[i * payload_size:(i + 1) * payload_size]
            logger.info('Fragment data.....Part %d-th, payload size:%d' % ((i + 1), len(part)))
            send(sock, get_send_bytes(0x01, part))
        part = data[(i + 1) * payload_size:]
        logger.info('Fragment data.....Part %d-th(final), payload size:%d' % ((i + 2), len(part)))
        send(sock, get_send_bytes(0x02, part))


if __name__ == '__main__':
    logger = logging.getLogger('udp_client')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logger.info('UDP socket created successfully...')
    except OSError as os_err:
        logger.error('Create socket, OSError: %s' % os_err)
        sys.exit(1)

    while True:
        try:
            logger.debug("Original data...\n%s" % detections)
            data = pickle.dumps(detections)
            logger.info('Pickle data length: %d bytes' % len(data))
            fragment_data(data)
        except KeyboardInterrupt as key_interrupt:
            logger.error('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.error('Exception: %s' % e)
            break

    logger.info('Close socket~~~')
    sock.close()
