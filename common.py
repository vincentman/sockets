from configparser import ConfigParser
import time


def load_config():
    config = {}
    parser = ConfigParser()
    parser.read('config.ini')
    config['host'] = parser['Server'].get('host', '127.0.0.1')
    config['port'] = parser['Server'].getint('port', '9990')
    config['queue_size_for_listen'] = parser['Server'].getint('queue_size_for_listen', '5')
    config['recv_buf_size'] = parser['Server'].getint('recv_buf_size', '4096')
    config['thread_pool_max_workers'] = parser['Server'].getint('thread_pool_max_workers', '4096')
    return config


def write_log(log_type, log_string, to_stdout=True):
    """
    write one line to log file
    """
    if to_stdout:
        print(log_string)
    file_name = '%s_%s' % (log_type, time.strftime("%Y-%m-%d.log", time.localtime()))
    prefix = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
    with open(file_name, 'at', encoding='utf-8') as file:
        file.write(prefix+'\t'+log_string+'\n')
