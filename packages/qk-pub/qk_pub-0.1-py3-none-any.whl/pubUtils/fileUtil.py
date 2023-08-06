import copy
import json
import math
import os
import tarfile
import threading
import time
from threading import Thread

from PyQt5.QtWidgets import QFileDialog

from pubConfig.FileConfig import ReadFileConfigEnum, calculate_t_num
from pubUtils import globalVar

multi_file_lock = threading.RLock()


def getFilePath():
    path = QFileDialog.getOpenFileName(globalVar.get_value("widget"), "选择文件")
    return path[0]


def exportFilePath(fileName="预解码解析数据_"):
    file_name = "{}_".format(fileName) + str(time.time()) + ".xlsx"
    return QFileDialog.getSaveFileName(globalVar.get_value("widget"), "保存文件", file_name)[0]


# 一行一行读
def readByLine(file_path, handleFunc):
    with open(file_path, 'r', encoding="utf8") as f:
        line = f.readline()
        while line:
            handleFunc(line)
        print("读取:{}完毕".format(file_path.split("\\")[-1]))


def readBylineMulThread(file_path, start_line_no, lines, handle_func):
    fileName = file_path.split("/")[-1].split(".")[0]
    fileNo = copy.deepcopy(start_line_no)
    for index, line in enumerate(lines):
        fileNo = fileNo + 1
        handle_func(line, fileNo)


def multi_thread_load_file(filePath: str, fileHandleFunc):
    globalVar.set_value(filePath, 0)
    start_time = time.time()
    file_lines = None
    with open(filePath, "r", encoding="UTF-8") as file:
        file_lines = file.readlines()
    """多线程遍历函数"""
    file_size = os.path.getsize(filePath)  # 获取文件大小用于分块
    thread_num = math.ceil(file_size / ReadFileConfigEnum.FILE_SPLIT_SIZE.value[0])
    thread_num = calculate_t_num(thread_num)

    thread_lst = []
    for i in range(thread_num):
        multi_file_lock.acquire()
        start = len(file_lines) // thread_num * i  # 计算当前分块开始位置
        end = len(file_lines) // thread_num * (i + 1)  # 计算当前分块结束位置
        lines = file_lines[start:end]
        start_line_no = start
        thread = Thread(target=readBylineMulThread, args=(filePath, start_line_no, lines, fileHandleFunc))
        thread.setName(filePath.split("\\")[-1] + "__thread" + str(i + 1) + "--->executing")
        thread.start()
        thread_lst.append(thread)
        multi_file_lock.release()

    [thread.join() for thread in thread_lst]
    # end_time = time.time()
    # print("解析 {} 文件耗时:{}s".format(filePath.split("\\")[-1], str((end_time - start_time))))


# 解压文件
def decompressionFile(tar_path, target_path):
    try:
        tar = tarfile.open(tar_path, "r:gz")
        file_names = tar.getnames()
        for file_name in file_names:
            tar.extract(file_name, target_path)
        tar.close()
    except Exception as e:
        print("解压 {} 文件失败 e:{}".format(tar_path, e))
        return False


# 读取json文件
def readJson(path):
    with open(path, "r", encoding='utf8') as f:
        jsonData = f.read()
        if jsonData:
            js = json.loads(jsonData)
            print("{} 读取完成".format(path.split("/")[-1]))
            return js
        return None


# 读取压缩文件
def readTarFile(file_path, fileHandleFunc=None):
    file_names = list()
    with tarfile.open(file_path, mode="r:gz") as gz:
        for number in gz.getmembers():
            f = gz.extractfile(number)
            number_path = number.path
            if not f:
                continue
            buff = f.read()
            # if "gz" in number_path:
            #     buff = gzip.decompress(buff).decode("utf-8")
            fileHandleFunc(number_path, buff)
            file_names.append(number_path)
            print("{} 文件 类型为：{}".format(number_path, number.type))
    return file_names


if __name__ == '__main__':
    file_path = "E:/pyworkspace/universal_tool/dev_tools/upload_files/10.35.1.8.tar.gz"
    readTarFile(file_path)
