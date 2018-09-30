import socket
import sys
from common import *
import pickle
import zlib

detections = [{"name": "name1", "age": 18, "gender": "male"}, {"name": "name2", "age": 20, "gender": "female"}]


if __name__ == '__main__':
    config = load_config()
    print('server config =>', config)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except OSError as os_err:
        write_log('server', '[ERROR]OSError: %s' % os_err)
        sys.exit(1)

    while True:
        try:
            # data = 'Hello! I am Vincent Kao from Taiwan.'.encode('utf-8')
            data = pickle.dumps(detections)
            data = zlib.compress(data)
            write_log('client', 'send %d bytes data...' % len(data))
            write_log('client', 'data...%s' % detections, False)
            sock.sendto(data, (config['host'], config['port']))
            time.sleep(1)
        except KeyboardInterrupt as key_interrupt:
            write_log('client', '[ERROR]KeyboardInterrupt')
            break
        except Exception as e:
            write_log('client', '[ERROR]Exception: %s' % e)
            break

    sock.close()
