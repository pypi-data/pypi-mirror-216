import json
import os
import time
from pathlib import Path

# curpath = os.path.realpath(__file__)  # 获取当前文件绝对路径
# dirpath = os.path.dirname(curpath)  # 获取当前文件的文件夹路径
dirpath = "d:\hasDoneEmptySlots"
emptySlotPath = os.path.join(dirpath, "doneScanEmptySlots.json")


def judgeFileExist(path):
    if not os.path.exists(dirpath):
        print("{}文件夹不存在开始创建".format(dirpath))
        os.makedirs(dirpath)
    if not os.path.exists(path):
        while not Path(dirpath).exists():
            print("等待{}文件创建成功".format(dirpath))
            time.time(0.5)
        print("{}文件不存在开始创建".format(path))
        file = open(path, 'w')
        file.close()

# 一行一行读


def readJson(path):
    judgeFileExist(path)
    with open(path, "r", encoding='utf8') as f:
        jsonData = f.read()
        if jsonData:
            js = json.loads(jsonData)
            print("读取完成")
            return js
        return None


def writeJson(jsonData, path):
    js = json.dumps(jsonData)
    with open(path, "w", encoding='utf8') as f:
        f.write(js)
        print("写入完成")


def readEmptySlots(path=emptySlotPath):
    return readJson(path)


def persistEmptySlots(slots, path=emptySlotPath):
    writeJson(slots, path)


if __name__ == '__main__':
    judgeFileExist(emptySlotPath)
