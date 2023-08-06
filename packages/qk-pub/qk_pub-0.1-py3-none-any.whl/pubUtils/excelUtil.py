import time

import xlwt
import pandas as pd
from PyQt5.QtWidgets import QFileDialog

from onoffline.service.agvInfoService import queryAgvCodeTypeMap
from pubUtils import globalVar, fileUtil
from pubUtils.dbUtil import getDbState
from pubUtils.httpUtil import fileRequest


def getFilePath():
    path = QFileDialog.getOpenFileName(globalVar.get_value("widget"), "选择文件")
    return path[0]


def upLoad(filePath, url):
    file = {"file": open(file=filePath, mode="rb")}
    res = fileRequest(url=url, files=file)
    return res


def list2JobMap(item, code_type_map):
    record = dict()
    record["start_time"] = item[0]
    record["agv_code"] = item[1][0]
    record["agv_type_code"] = code_type_map.get(record["agv_code"])
    record["state"] = item[1][1]
    record["diff_time"] = item[1][2]

    return record


def export_excel(export):
    ui = globalVar.get_value("ui")
    if not getDbState():
        ui.log_show_area.append("db:{}-->未连接".format(ui.service_ip.text()))
        return
    code_type_map = queryAgvCodeTypeMap()
    jobs = list(map(lambda item: list2JobMap(item, code_type_map), export))

    # 将字典列表转换为DataFrame
    pf = pd.DataFrame(jobs)
    # 指定字段顺序
    order = ['start_time', 'state', 'agv_code', 'agv_type_code', 'diff_time']
    pf = pf[order]
    time.sleep(1)
    # 将列名替换为中文
    columns_map = {
        'start_time': '掉线时间',
        'agv_code': 'agv编码',
        'agv_type_code': "AGV类型",
        'state': "状态",
        'diff_time': "时差/s"
    }
    pf.rename(columns=columns_map, inplace=True)
    # 指定生成的Excel表格名称
    filePath = fileUtil.exportFilePath(fileName="onoffline_record")
    if not filePath:
        print("请选择文件保存路径")
        return False
    file_path = pd.ExcelWriter(filePath)
    # 替换空单元格
    pf.fillna(' ', inplace=True)
    # 输出
    pf.to_excel(file_path, encoding='utf-8', index=False)
    # 保存表格
    file_path.save()
    print("导出成功！！！")
    return True
