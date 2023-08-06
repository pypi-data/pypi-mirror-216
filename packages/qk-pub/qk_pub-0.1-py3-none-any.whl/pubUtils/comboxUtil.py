import copy
from PyQt5 import QtCore, QtGui, QtWidgets


class CheckableComboBox(QtWidgets.QComboBox):
    queryInfo = None

    def __init__(self, layout=None, parent=None, bindBox=None, firstItem=None):
        super(CheckableComboBox, self).__init__(parent)
        # self.setFixedWidth(200)
        self.setMaximumWidth(400)
        self.setMinimumWidth(200)
        self.firstItem = firstItem
        self.setModel(QtGui.QStandardItemModel(self))
        self.view().pressed.connect(self.handleItemPressed)
        self.checkedItems = []
        self.lastCheckedItems = []
        self.valueChanged = False
        self.view().pressed.connect(self.get_all)
        self.view().pressed.connect(self.getCheckItem)
        self.status = 0
        self.setObjectName("roadway_codes_box")
        layout.insertWidget(3, self)
        self.clear()
        if firstItem:
            self.addItem(firstItem)
        self.bindBox = bindBox
        # box = self

    # def hidePopup(self):
    #     print("收起:",self.checkedItems)
    #     QComboBox.hidePopup(self)
    def init_dt(self, dts=None):
        if dts:
            self.clear()
            if self.firstItem:
                self.addItem(self.firstItem)
            self.addItems(dts)
            return
        if self.queryInfo:
            self.addItems(self.queryInfo())
            return

    def setQueryFunc(self, func):
        self.queryInfo = func

    def init_bind_data(self, data=None):
        print("开始初始化下拉")
        if not data:
            print("CheckedComboBox init_data param is None")
            self.bindBox.clear()
            # return
        self.bindBox.clear()
        if self.bindBox.firstItem:
            self.bindBox.addItem(self.bindBox.firstItem)
        if self.bindBox.queryInfo and data:
            dts = self.bindBox.queryInfo(data)
            if dts:
                self.bindBox.addItems(dts)

    def handleItemPressed(self, index):  # 这个函数是每次选择项目时判断状态时自动调用的，不用管（自动调用）
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def getCheckItem(self):
        self.lastCheckedItems = copy.deepcopy(self.checkedItems)
        # getCheckItem方法可以获得选择的项目列表，自动调用。
        for index in range(1, self.count()):
            item = self.model().item(index)
            if item.checkState() == QtCore.Qt.Checked:
                if item.text() not in self.checkedItems:
                    self.checkedItems.append(item.text())
            else:
                if item.text() in self.checkedItems:
                    self.checkedItems.remove(item.text())
        self.valueChanged = True if self.lastCheckedItems != self.checkedItems else False
        return self.checkedItems  # 实例化的时候直接调用这个self.checkedItems就能获取到选中的值，不需要调用这个方法，方法会在选择选项的时候自动被调用。

    def get_all(self):  # 实现全选功能的函数（自动调用）
        all_item = self.model().item(0)
        for index in range(1, self.count()):  # 判断是否是全选的状态，如果不是，全选按钮应该处于未选中的状态
            if self.status == 1:
                if self.model().item(index).checkState() == QtCore.Qt.Unchecked:
                    all_item.setCheckState(QtCore.Qt.Unchecked)
                    self.status = 0
                    break
        if all_item.checkState() == QtCore.Qt.Checked:
            if self.status == 0:
                for index in range(self.count()):
                    self.model().item(index).setCheckState(QtCore.Qt.Checked)
                    self.status = 1
        elif all_item.checkState() == QtCore.Qt.Unchecked:
            for index in range(self.count()):
                if self.status == 1:
                    self.model().item(index).setCheckState(QtCore.Qt.Unchecked)
            self.status = 0

    def get_checkedItems_slot(self):
        print("get_checkedItems_slot res:{}".format(self.checkedItems))
        if self.bindBox:
            self.init_bind_data(self.checkedItems)
        return self.checkedItems
