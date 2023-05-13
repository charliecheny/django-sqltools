"""
封装log方法
"""

import logging
import os,sys
import time
import platform

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

logger = logging.getLogger()
level = 'default'

def create_file(filename):
    '''
    # 先判断文件路径是否存在，不存在的话就先创建目录结构
    # 再判断文件名是否存在，不存在就创建文件
    :param filename:接受完整的文件名
    '''
    # 判断是否是windows系统
    if platform.system() == "Windows":
        path = filename[0:filename.rfind('\\')]
    else:
        path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass

def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.err_handler)
    else:
        logger.addHandler(MyLog.handler)

def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    else:
        logger.removeHandler(MyLog.handler)

# 定义日志的输出时间格式
def get_current_time():
    return time.strftime(MyLog.date, time.localtime(time.time()))

class MyLog:
    # 获取当前项目的目录(看日志文件所在位置，维护其顶级目录位置)
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # 判断当前时间的目录在日志目录结构中是否存在，存在就不创建，不存在就创建
    dir_time = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    log_file = os.path.join(os.path.join(os.path.join(path,"Log"),"log"),'{}.log'.format(dir_time))
    err_file = os.path.join(os.path.join(os.path.join(path,"Log"),"err"),'{}.err.log'.format(dir_time))
    logger.setLevel(LEVELS.get(level, logging.NOTSET))
    create_file(log_file)
    create_file(err_file)
    date = '%Y-%m-%d %H:%M:%S'     # 定义日志格式

    # 设置
    handler = logging.FileHandler(log_file, encoding='utf-8')
    err_handler = logging.FileHandler(err_file, encoding='utf-8')

    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        logger.debug("[DEBUG " + get_current_time() + "]" + str(log_meg))
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        logger.info("[INFO " + get_current_time() + "]" + str(log_meg))
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        logger.warning("[WARNING " + get_current_time() + "]" + str(log_meg))
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        set_handler('error')
        logger.error("[ERROR " + get_current_time() + "]" + str(log_meg))
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        logger.error("[CRITICAL " + get_current_time() + "]" + str(log_meg))
        remove_handler('critical')

# 调试用的main函数
# if __name__ == "__main__":
    # MyLog.debug("This is debug message")
    # MyLog.info("This is info message3")
    # MyLog.warning("This is warning message")
    # MyLog.error("This is error3")
    # MyLog.critical("This is critical message")