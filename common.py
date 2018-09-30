from configparser import ConfigParser
import time


def get_server_config():
    config = {}
    parser = ConfigParser()
    parser.read('server.ini')
    config['host'] = parser['Default'].get('host', '127.0.0.1')
    config['port'] = parser['Default'].getint('port', '9990')
    config['connections'] = parser['Default'].getint('connections', '10')
    config['recv_buf_size'] = parser['Default'].getint('recv_buf_size', '4096')
    return config


# def write_client_log(log_string, to_stdout=True):
#     if to_stdout:
#         print(log_string)
#     file_name = time.strftime("client_%Y-%m-%d.log", time.localtime())
#     with open(file_name, 'at', encoding='utf-8') as file:
#         file.write(log_string+'\n')



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
