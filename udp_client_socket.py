import socket
import sys
from common import *
import pickle
import zlib

detections = [{"name": "name1", "age": 18, "gender": "male"}, {"name": "name2", "age": 20, "gender": "female"}]


def send(sock, data):
    logger.info('Send %d bytes data...' % len(data))
    sent_bytes = sock.sendto(data, (config['host'], config['port']))
    logger.info('%d bytes data sent...' % sent_bytes)
    if len(data) != sent_bytes:
        logger.warning('Not all data sent completely!!')
    time.sleep(1)


def get_send_bytes(header, payload):
    send_bytes = bytearray()
    send_bytes.append(header)
    send_bytes.extend(payload)
    return send_bytes


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
            # with open('temp', 'wb') as f:
            #     f.write(detections)
            # with open('temp', 'rb') as f:
            #     print(f.read(60))
            # [d[i:i + 1] for i in range(len(data))]
            payload_size = config['recv_buf_size'] - 1
            data = pickle.dumps(detections)
            if len(data) <= payload_size:
                send(sock, get_send_bytes(0x02, data))
            else:
                # if len(data) % payload_size == 0:
                #     chunks = len(data) // payload_size
                #     for i in range(chunks - 1):
                #         part = data[i * payload_size:(i + 1) * payload_size]
                #         send(sock, get_send_bytes(0x01, part))
                #     part = data[(i + 1) * payload_size:len(data)]
                #     send(sock, get_send_bytes(0x02, part))
                # else:
                #     chunks = len(data) // payload_size + 1
                #     for i in range(chunks-1):
                #         part = data[i * payload_size:(i + 1) * payload_size]
                #         send(sock, get_send_bytes(0x01, part))
                #     part = data[(i + 1) * payload_size:len(data)]
                #     send(sock, get_send_bytes(0x02, part))
                if len(data) % payload_size == 0:
                    chunks = len(data) // payload_size
                else:
                    chunks = len(data) // payload_size + 1
                for i in range(chunks - 1):
                    part = data[i * payload_size:(i + 1) * payload_size]
                    send(sock, get_send_bytes(0x01, part))
                part = data[(i + 1) * payload_size:len(data)]
                send(sock, get_send_bytes(0x02, part))

            # data = pickle.dumps(detections)
            # data = zlib.compress(data)
            # if len(data) > config['recv_buf_size']:
            #     logger.warning('Data exceeds server buffer size. Drop data!!')
            #     time.sleep(1)
            #     continue
            # logger.info('Send %d bytes data...' % len(data))
            # logger.debug('Data...%s' % detections)
            # sent_bytes = sock.sendto(data, (config['host'], config['port']))
            # logger.info('%d bytes data sent...' % sent_bytes)
            # if len(data) != sent_bytes:
            #     logger.warning('Not all data sent completely!!')
            # time.sleep(1)
        except KeyboardInterrupt as key_interrupt:
            logger.error('KeyboardInterrupt~~~')
            break
        except Exception as e:
            logger.error('Exception: %s' % e)
            break

    logger.info('Close socket~~~')
    sock.close()
