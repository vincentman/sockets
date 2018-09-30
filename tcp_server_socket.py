import socket
import sys
from common import *
import pickle
import zlib
from concurrent.futures import ThreadPoolExecutor


def do_recv(csock, host, port):
    count = 0
    while True:
        try:
            data = csock.recv(config['recv_buf_size'])
            if not data:
                write_log('server', 'Received 0 bytes data from %s:%d.' % (host, port))
                break
            else:
                count += 1
                write_log('server', '+%d Received %d bytes data from %s:%d' % (count, len(data), host, port))
                data = zlib.decompress(data)
                detections = pickle.loads(data)
                write_log('server', 'Data...%s' % detections, False)
        except KeyboardInterrupt:
            write_log('server', '[ERROR]KeyboardInterrupt')
            break
        except Exception as e:
            write_log('server', '[ERROR]Exception: %s' % e)
            break

    write_log('server', 'Close socket for client(%s:%d).' % (host, port))
    csock.close()


if __name__ == '__main__':
    config = load_config()
    print('config =>', config)

    pool = ThreadPoolExecutor(config['thread_pool_max_workers'])

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        write_log('server', 'TCP socket created successfully...')
    except OSError as os_err:
        write_log('server', '[ERROR]Create socket, OSError: %s' % os_err)
        sys.exit(1)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse socket
    sock.bind((config['host'], config['port']))
    sock.listen(config['queue_size_for_listen'])

    while True:
        try:
            (csock, (host, port)) = sock.accept()
            write_log('server', 'Accept from %s:%d' % (host, port))
            pool.submit(do_recv, csock, host, port)
        except KeyboardInterrupt:
            write_log('server', '[ERROR]KeyboardInterrupt')
            break
        except Exception as e:
            write_log('server', '[ERROR]Exception: %s' % e)
            break

    write_log('server', 'Close server socket~~~')
    sock.close()
