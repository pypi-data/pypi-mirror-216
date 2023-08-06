import time
from datetime import datetime


def currData():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def getToday():
    return time.strftime("%Y-%m-%d", time.localtime())


def date2ms(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp() * 1000


def date2ms_v2(dt):
    return date2ms(dt.split(",")[0]) + int(dt.split(",")[-1])


def date2msCommon(date):
    if "," in date:
        return date2ms_v2(date)
    return date2ms(date)


def ms2Date(ms):
    return datetime.fromtimestamp(ms / 1000)


def parse2Date(dt):
    date = ms2Date(date2ms(dt.split(",")[0]) + int(dt.split(",")[-1]))
    return date


def parse2Date_v2(dt):
    return ms2Date(date2ms(dt))


if __name__ == '__main__':
    # print(getToday())
    # print(currData())

    # print(date2ms_v2("2023-05-05 14:59:41,734"))
    print(date2msCommon("2023-05-05 14:59:41,734"))
    print(str(date2msCommon("2023-05-05 14:59:41")) > "")
