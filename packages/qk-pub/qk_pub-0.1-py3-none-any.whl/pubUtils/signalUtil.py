import time

from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QWidget, QMessageBox

from utils import globalVar
from utils.decoratorUtil import no_daemon_async

lastTimesTamp = None


@no_daemon_async
def showInfo(data):
    # print("data:{}".format(data))
    global lastTimesTamp
    currTimeStamp = time.time()
    if lastTimesTamp and (currTimeStamp - lastTimesTamp) < 1:
        return
    lastTimesTamp = currTimeStamp
    QMessageBox.information(globalVar.get_value("widget"), data.get("title"), data.get("msg")).Close


class InfoSignal(QObject):
    signal_dict = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.signal_dict.connect(showInfo)

    def emit(self, title="提示框", msg=None):
        self.signal_dict.emit({"title": title, "msg": msg})


# @nor_async
def updateUIInfo(data):
    func = data.get("func")
    args = data.get("args", None)
    if not args:
        func()
        return
    func(args)


uiSignal = None


class UISignal(QObject):
    signal_dict = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.signal_dict.connect(updateUIInfo)

    def emit(self, func=None, args=None, kwargs=None):
        self.signal_dict.emit({"func": func, "args": args, "kwargs": kwargs})


def update_ui_info(func, args=None, kwargs=None):
    global uiSignal
    if not uiSignal:
        uiSignal = UISignal()
    uiSignal.emit(func, args, kwargs)


if __name__ == '__main__':
    # sig = InfoSignal()
    # sig.emit(msg="你大爷")
    def tt(*args, **kwargs):
        print(args[0] + args[1])


    update_ui_info(func=tt, args=(1, 2))
