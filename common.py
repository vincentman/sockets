from configparser import ConfigParser
import time
import logging


def load_config():
    config = {}
    parser = ConfigParser()
    parser.read('config.ini')
    config['host'] = parser['Server'].get('host', '127.0.0.1')
    config['port'] = parser['Server'].getint('port', '9990')
    config['queue_size_for_listen'] = parser['Server'].getint('queue_size_for_listen', '15')
    config['recv_buf_size'] = parser['Server'].getint('recv_buf_size', '4096')
    config['thread_pool_max_workers'] = parser['Server'].getint('thread_pool_max_workers', '15')
    config['basic_log_level'] = parser['Default'].get('basic_log_level', 'DEBUG')
    config['console_log_level'] = parser['Default'].get('console_log_level', 'INFO')
    config['to_server_host'] = parser['Client'].get('to_server_host', '127.0.0.1')
    config['to_server_port'] = parser['Client'].getint('to_server_port', '9990')
    return config


def get_logging_level(log_level):
    switcher = {
        'FATAL': logging.FATAL,
        'ERROR': logging.ERROR,
        'WARN': logging.WARN,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }
    return switcher.get(log_level, logging.NOTSET)


def set_logging(config):
    console = logging.StreamHandler()
    console.setLevel(get_logging_level(config['console_log_level']))
    formatter = logging.Formatter('%(name)-12s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    log_file_name = '%s.log' % (time.strftime("%Y-%m-%d", time.localtime()))
    logging.basicConfig(level=get_logging_level(config['basic_log_level']),
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M',
                        handlers=[logging.FileHandler(log_file_name, 'a', 'utf-8'), console])


config = load_config()
print('config =>', config)

set_logging(config)
