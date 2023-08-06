import logging
import os
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))


def set_log(level, log_path, log_size, log_backup_count):
    # 设置日志的记录等级
    # logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径（前面的logs为文件的名字，需要我们手动创建，后面则会自动创建）、每个日志文件的最大大小、保存的日志文件个数上限。
    file_log_handler = RotatingFileHandler(filename=log_path, maxBytes=log_size, encoding="utf-8",
                                           backupCount=log_backup_count)
    # 创建日志记录的格式               日志等级    输入日志信息的文件名   行数       日志信息
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logger = logging.getLogger("dd.yy")
    logger.setLevel(level)
    logger.addHandler(file_log_handler)
