import enum


class ReadFileConfigEnum(enum.Enum):
    MAX_THREAD_NUM = 50, "最大线程数"
    MIDDLE_THREAD_NUM = 25, "居中线程数"
    MIN_THREAD_NUM = 10, "最小线程数"
    FILE_SPLIT_SIZE = 1024 * 1024 * 3, "文件分块大小默认2M 用来做多线程文件读取"


def calculate_t_num(thread_num: int):
    if thread_num >= ReadFileConfigEnum.MAX_THREAD_NUM.value[0]:
        return ReadFileConfigEnum.MAX_THREAD_NUM.value[0]

    return thread_num


if __name__ == '__main__':
    print(ReadFileConfigEnum.MIDDLE_THREAD_NUM.value[0])
