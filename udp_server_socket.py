import socket
import sys
from common import *
import pickle
import zlib


if __name__ == '__main__':
    config = load_config()
    print('config =>', config)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        write_log('server', 'UDP socket created successfully...')
    except OSError as os_err:
        write_log('server', '[ERROR]Create socket, OSError: %s' % os_err)
        sys.exit(1)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse socket
    sock.bind((config['host'], config['port']))

    while True:
        try:
            data, (host, port) = sock.recvfrom(config['recv_buf_size'])
            if not data:
                print('No data received...')
            else:
                write_log('server', 'Received %d bytes data from %s:%d' % (len(data), host, port))
                data = zlib.decompress(data)
                detections = pickle.loads(data)
                write_log('server', 'Data...%s' % detections, False)
        except KeyboardInterrupt:
            write_log('server', '[ERROR]KeyboardInterrupt')
            break
        except Exception as e:
            write_log('server', '[ERROR]Exception: %s' % e)
            break

    write_log('server', 'Close socket~~~')
    sock.close()
