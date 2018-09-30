import socket
import sys
from common import *
import pickle
import zlib

detections = [{"name": "name1", "age": 18, "gender": "male"}, {"name": "name2", "age": 20, "gender": "female"}]


if __name__ == '__main__':
    config = load_config()
    print('config =>', config)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        write_log('client', 'TCP socket created successfully...')
    except OSError as os_err:
        write_log('client', '[ERROR]Create socket, OSError: %s' % os_err)
        sys.exit(1)

    try:
        sock.connect((config['host'], config['port']))
    except OSError as os_err:
        write_log('client', '[ERROR]Connect socket, OSError: %s' % os_err)
        sys.exit(1)

    while True:
        try:
            data = pickle.dumps(detections)
            data = zlib.compress(data)
            if len(data) > config['recv_buf_size']:
                write_log('client', '[WARN]Data exceeds buffer size of server. Drop data!!')
                time.sleep(1)
                continue
            write_log('client', 'Send %d bytes data...' % len(data))
            write_log('client', 'Data...%s' % detections, False)
            sent_bytes = sock.send(data)
            write_log('client', '%d bytes data sent...' % sent_bytes)
            if len(data) != sent_bytes:
                write_log('client', '[WARN]Not all data sent completely!!')
            time.sleep(1)
        except KeyboardInterrupt as key_interrupt:
            write_log('client', '[ERROR]KeyboardInterrupt')
            break
        except Exception as e:
            write_log('client', '[ERROR]Exception: %s' % e)
            break

    write_log('client', 'Close socket~~~')
    sock.close()
