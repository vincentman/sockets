import socket
import sys
from common import *
import pickle
import zlib
import logging

client_data = {}


def assemble_data(data, client):
    if client not in client_data:
        bs = bytearray()
        if data[0] == b'0x02':
            logger.info('Assemble data, data have only one part...')
    else:
        bs = client_data[client]
    bs.extend(data[1:])
    # logger.info('Assemble data, header:0x%02x, payload size:%d' % (data[0], len(data[1:])))
    if data[0] == 0x02:
        logger.info('Assemble data, final part, payload size:%d' % len(data[1:]))
        logger.info('Data merged from %s, data size:%d' % (client, len(bs)))
        client_data.update({client: bytearray()})
        return bs
    elif data[0] == 0x01:
        logger.info('Assemble data, payload size:%d' % len(data[1:]))
        client_data.update({client: bs})


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
            recv_bytes, (host, port) = sock.recvfrom(config['recv_buf_size'])
            if not recv_bytes:
                print('No data received...')
            else:
                logger.info('UDP socket, received %d bytes data from %s:%d' % (len(recv_bytes), host, port))
                data = assemble_data(recv_bytes, '%s:%d' % (host, port))
                if data != None:
                    # data = zlib.decompress(data)
                    detections = pickle.loads(data)
                    logger.debug("Original Data...\n%s" % detections)
        except KeyboardInterrupt:
            logger.error('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.error('Exception: %s' % e)
            break

    logger.info('Close socket~~~')
    sock.close()
