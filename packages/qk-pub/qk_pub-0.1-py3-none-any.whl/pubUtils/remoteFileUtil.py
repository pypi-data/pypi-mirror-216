import copy
import gzip
import io
import math
import os
import stat
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import paramiko

from onoffline.entity.onofflineDO import LogFileRecordDo
from pubConfig.FileConfig import ReadFileConfigEnum, calculate_t_num
from pub_dao.sqliteDao import LogFileDao


class RemoteFileUtil:
    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("multi_file_lock")
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # 重新绑定移除的属性
        self.multi_file_lock = threading.RLock()

    def __init__(self, service_ip=None, port=22, username="root", password="123456", max_workers=30,
                 logFileClient: LogFileDao = None):
        self.service_ip = service_ip
        self.port = port
        self.username = username
        self.password = password
        self.max_workers = max_workers

        # 对paramiko的SSHclient类进行实例化
        self.ssh = paramiko.SSHClient()
        # 设置应对策略，AutoAddPolic自动添加服务器到know_hosts文件
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.multi_file_lock = threading.RLock()

        # 压缩文件和行映射
        # self.zipFile_lines_map = dict()
        # self.zipFile_lines_map_lock = threading.RLock()
        self.logFileClient = logFileClient
        # 每个文件的任务包
        self.file_read_task_map = dict()

    def connect(self):
        # 输入服务器地址，账户名，密码
        self.ssh.connect(hostname=self.service_ip, port=self.port, username=self.username,
                         password=self.password, banner_timeout=10000, timeout=math.inf, compress=False)
        self.ftpClient = self.ssh.open_sftp()

    def close(self):
        self.ftpClient.close()
        self.ssh.close()

    def is_dir(self, path):
        return stat.S_ISDIR(path.st_mode)

    def is_file(self, path):
        return stat.S_ISREG(path.st_mode)

    def file_sizeM(self, path):
        with self.ftpClient.open(path) as f:
            return f.stat().st_size / (1024 * 1024)

    def execute_cmd(self, cmds: list):
        stdin, stdon, stderr = self.ssh.exec_command(";".join(cmds))
        print(stdon.read().decode('utf-8', errors="ignore"))
        # 返回错误的执行结果(以byte形式返回，可以使用decode进行解码成字符串)，如果正确则返回空
        print(stderr.read().decode('utf-8', errors="ignore"))
        return stdon.read().decode('utf-8', errors="ignore"), stderr.read().decode('utf-8', errors="ignore")

    def filter(self, filePath, handle):
        with self.ftpClient.open(filePath, "r") as file:
            file_lines = file.readlines()
        return handle(file_lines)

    def readLineDatas(self, file_path, lines, endFileNo, handle_func):
        fileNo = endFileNo
        for index, line in enumerate(lines):
            fileNo += 1
            print("{} 线程 读取{}文件 lineNo:{}".format(threading.current_thread().name, file_path, fileNo))
            if handle_func(file_path, line, lines, fileNo, self.file_read_task_map.get(file_path)):
                print("{} 文件读取结束".format(file_path))
                return

    def catHeadLine(self, filePath, head=1):
        if filePath.endswith("gz"):
            if not self.logFileClient or not self.logFileClient.exist(filePath):
                stdin, stdout, stderr = self.ssh.exec_command("cat {} ".format(filePath))
                content = stdout.read()
                file_lines = gzip.decompress(content).decode("utf-8").split("\n")
                if self.logFileClient:
                    records = [LogFileRecordDo(file_path=filePath, line=line) for line in file_lines]
                    self.logFileClient.batchInsert(records=records)
                return file_lines[0:head]
            return [record.get("line") for record in self.logFileClient.queryByfilePath(file_path=filePath)[0:head]]
        else:
            stdin, stdout, stderr = self.ssh.exec_command("cat {} | head -n {}".format(filePath, head))
            content = stdout.read()
            buff = io.BytesIO(content)
            return [str(line, encoding="utf-8", errors="ignore") for line in buff.readlines()]

    def catTailLine(self, filePath, tail=1):
        if filePath.endswith("gz"):
            if not self.logFileClient or not self.logFileClient.exist(filePath):
                stdin, stdout, stderr = self.ssh.exec_command("cat {} ".format(filePath))
                content = stdout.read()
                file_lines = gzip.decompress(content).decode("utf-8").split("\n")
                if self.logFileClient:
                    records = [LogFileRecordDo(file_path=filePath, line=line) for line in file_lines]
                    self.logFileClient.batchInsert(records=records)
                return file_lines[-(tail + 1):-1]
            return [record.get("line") for record in
                    self.logFileClient.queryByfilePath(file_path=filePath)[-(tail + 1):-1]]
        else:
            stdin, stdout, stderr = self.ssh.exec_command("cat {} | tail -n {}".format(filePath, tail))
            content = stdout.read()
            buff = io.BytesIO(content)
            return [str(line, encoding="utf-8", errors="ignore") for line in buff.readlines()]

    def readFile2LinesByCat(self, filePath, readFilterFunc, handle_func):
        if self.logFileClient and self.logFileClient.exist(filePath):
            self.readGZFile(filePath=filePath, fileHandleFunc=handle_func)
        else:
            endFileNo = 0
            tasks = []
            stdin, stdout, stderr = self.ssh.exec_command("cat {} ".format(filePath))
            with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="cat_read__executor") as f:
                while True:
                    lines = stdout.readlines(1024 * 1024 * 2)
                    if not lines or readFilterFunc(lines):
                        break
                    print("{} 进程 读取{}文件".format(os.getpid(), filePath))
                    t_job = f.submit(self.readLineDatas, filePath, lines, endFileNo, handle_func)
                    tasks.append(t_job)
                    endFileNo += len(lines)
            self.file_read_task_map.__setitem__(filePath, tasks)
            for future in as_completed(tasks):
                data = future.result()
                print("{} 文件执行完成回调".format(filePath, data))

    def readBylineMulThread(self, file_path, start_line_no, lines, handle_func):
        fileNo = copy.deepcopy(start_line_no)
        for index, line in enumerate(lines):
            fileNo = fileNo + 1
            if not line:
                continue
            print("{} 线程 读取{}文件 lineNo:{}".format(threading.current_thread().name, file_path, fileNo))
            if handle_func(file_path, line, lines, fileNo, self.file_read_task_map.get(file_path)):
                print("{} 文件读取结束".format(file_path))
                return

    def readGZFile(self, filePath, readFilterFunc, fileHandleFunc):
        with self.ftpClient.open(filePath, "r") as file:
            file_size = file.stat().st_size
        """多线程遍历函数"""
        thread_num = math.ceil(file_size / ReadFileConfigEnum.FILE_SPLIT_SIZE.value[0])
        thread_num = calculate_t_num(thread_num)
        stdin, stdout, stderr = self.ssh.exec_command("cat {} ".format(filePath))
        if "gz" in filePath:
            file_lines = gzip.decompress(stdout.read()).decode("utf-8", errors="ignore").split("\n")
        else:
            file_lines = stdout.read().decode("utf-8", errors="ignore").split("\n")
        tasks = list()
        with ThreadPoolExecutor(max_workers=thread_num, thread_name_prefix="gz_read__executor") as t:
            for i in range(thread_num):
                self.multi_file_lock.acquire()
                start = len(file_lines) // thread_num * i  # 计算当前分块开始位置
                end = len(file_lines) // thread_num * (i + 1)  # 计算当前分块结束位置
                lines = file_lines[start:end]
                if readFilterFunc(lines):
                    return
                start_line_no = start
                print("{} 进程 读取{}文件".format(os.getpid(), filePath))
                task = t.submit(self.readBylineMulThread, filePath, start_line_no, lines, fileHandleFunc)
                tasks.append(task)
                self.multi_file_lock.release()
            self.file_read_task_map.__setitem__(filePath, tasks)
            for future in as_completed(tasks):
                data = future.result()
                print("{} 文件执行完成回调".format(filePath, data))

    def readFile2linesByOpen(self, filePath):
        total_lines = list()
        with self.ftpClient.open(filePath, mode="r:gz", bufsize=1024 * 1024 * 5) as f:
            while True:
                lines = f.readlines(1024 * 1024)
                if not lines:
                    break
                total_lines.extend(lines)
        return total_lines

    def multi_thread_load_file(self, filePath: str, readFilterFunc, fileHandleFunc):
        fileSize = self.file_sizeM(filePath)
        start_time = time.time()
        # if filePath.endswith("gz"):
        self.readGZFile(filePath, readFilterFunc, fileHandleFunc)
        # else:
        #     self.readFile2LinesByCat(filePath, readFilterFunc, fileHandleFunc)
        end_time = time.time()
        print("解析 {}  文件{}M 耗时:{}s 总耗时:{}".format(filePath, fileSize,
                                                           str((end_time - start_time)),
                                                           end_time - start_time))


if __name__ == '__main__':
    remoteFileUtil = RemoteFileUtil(service_ip="172.31.238.174")
    # remoteFileUtil.execute_cmd(["cd /opt/docker/evo-rcs/logs", "pwd", "ls"])
    ftpClient = remoteFileUtil.ftpClient
    agv_name_prex = ["CARRIER"]
    ftpClient.chdir("/opt/docker/evo-rcs/logs/agv_logs")
    agv_dirs_attrs = list(
        filter(lambda item: item.filename.split("_")[0] in agv_name_prex and remoteFileUtil.is_dir(item),
               ftpClient.listdir_attr("./")))
    agv_dir_paths = list(map(lambda item: item.filename, agv_dirs_attrs))
    [print(filePath) for filePath in agv_dir_paths]
    remoteFileUtil.multi_thread_load_file(
        filePath="/opt/docker/evo-rcs/logs/agv_logs/CARRIER_192168001001/rcs_command.log",
        # 2023-06-03-18.1.gz
        fileHandleFunc=lambda line, lineNo: print(line, lineNo))
    # remoteFileUtil.multi_thread_load_file(filePath="/opt/docker/evo-rcs/logs/gc.log",
    #                                       fileHandleFunc=lambda line, lineNo: print(line, lineNo))
