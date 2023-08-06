import math
import os
import time
from functools import wraps
from threading import Thread
from PyQt5.QtWidgets import QMessageBox

from pubUtils import globalVar


def btn_async(title=None, msg=None):
    def btn_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if msg:
                if QMessageBox.Yes == QMessageBox.question(globalVar.get_value("widget"), title, msg,
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes):
                    thr = Thread(target=func, args=args, kwargs=kwargs)
                    thr.setDaemon(True)
                    thr.start()

        return wrapper

    return btn_func


def nor_async(t_name=None):
    def normal_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            thr = Thread(target=func, args=args, kwargs=kwargs)
            thr.setDaemon(True)
            if t_name:
                thr.setName(t_name)
            thr.start()
            return wrapper

    return normal_func


def cm_async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.setDaemon(True)
        thr.start()
        return thr

    return wrapper


def no_daemon_async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.setDaemon(False)
        thr.start()

    return wrapper


def test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        file_path = args[0]
        file_name = file_path.split("\\")[-1]
        print("{} 函数开始调用".format(func.__name__))
        func(*args, **kwargs)
        print("{} 函数调用结束".format(func.__name__))
        end_time = time.time()
        print("读取 {} 耗时--->{}s".format(file_name, math.ceil((end_time - start_time))))
        # 读取完成后删除文件
        os.remove(file_path)

    return wrapper


if __name__ == '__main__':
    # dt = []
    # dt.insert(1, 52)
    # dt.insert(0, 53)
    dt = []
    print(dt[1:])
