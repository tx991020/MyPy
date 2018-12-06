
import logging
import logging.config

def get_log():
    """
    description: 日志处理函数
    :return: 返回一个日志实例
    """
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('pom')

    return logger