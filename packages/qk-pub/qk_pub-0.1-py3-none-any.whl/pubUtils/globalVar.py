import threading

lock = threading.RLock()


def _init():
    """ 初始化 """

    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """ 定义一个全局变量 """
    try:
        lock.acquire()
        _global_dict[key] = value
    finally:
        lock.release()


def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        lock.acquire()
        v = _global_dict[key]
        lock.release()
        return v if v or v == 0 else defValue

    except KeyError:  # 查找字典的key不存在的时候触发
        lock.release()
        return defValue
