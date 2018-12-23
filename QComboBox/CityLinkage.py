#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月27日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: ComboBox
@description: 
'''
import json
import sys

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QComboBox,\
    QLabel, QSpacerItem, QSizePolicy
import chardet


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, *args, **kwargs):
        super(SortFilterProxyModel, self).__init__(*args, **kwargs)
        self.setFilterRole(Qt.ToolTipRole)  # 根据Qt.ToolTipRole角色过滤
        self._model = QStandardItemModel(self)
        self.setSourceModel(self._model)

    def appendRow(self, item):
        self._model.appendRow(item)

    def setFilter(self, _):
        # 过滤
        # self.sender()#发送者
        # 获取上一个下拉框中的item_code
        item_code = self.sender().currentData(Qt.ToolTipRole)
        if not item_code:
            return
        if item_code.endswith("0000"):  # 过滤市
            self.setFilterRegExp(QRegExp(item_code[:-4] + "\d\d00"))
        elif item_code.endswith("00"):  # 过滤市以下
            self.setFilterRegExp(QRegExp(item_code[:-2] + "\d\d"))


class CityLinkageWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(CityLinkageWindow, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        self.province_box = QComboBox(self, minimumWidth=200)  # 市级以上
        self.city_box = QComboBox(self, minimumWidth=200)  # 市
        self.county_box = QComboBox(self, minimumWidth=200)  # 市级以下
        layout.addWidget(QLabel("省/直辖市/特别行政区", self))
        layout.addWidget(self.province_box)
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(QLabel("市", self))
        layout.addWidget(self.city_box)
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(QLabel("区/县", self))
        layout.addWidget(self.county_box)
        self.initModel()
        self.initSignal()
        self.initData()

    def initSignal(self):
        # 初始化信号槽
        self.province_box.currentIndexChanged.connect(
            self.city_model.setFilter)
        self.city_box.currentIndexChanged.connect(self.county_model.setFilter)

    def initModel(self):
        # 初始化模型
        self.province_model = SortFilterProxyModel(self)
        self.city_model = SortFilterProxyModel(self)
        self.county_model = SortFilterProxyModel(self)
        # 设置模型
        self.province_box.setModel(self.province_model)
        self.city_box.setModel(self.city_model)
        self.county_box.setModel(self.county_model)

    def initData(self):
        # 初始化数据
        datas = open("Data/data.json", "rb").read()
        encoding = chardet.detect(datas) or {}
        datas = datas.decode(encoding.get("encoding", "utf-8"))
        datas = json.loads(datas)
        # 开始解析数据
        for data in datas:
            item_code = data.get("item_code")  # 编码
            item_name = data.get("item_name")  # 名字
            item = QStandardItem(item_name)
            item.setData(item_code, Qt.ToolTipRole)
            if item_code.endswith("0000"):  # 4个0结尾的是市级以上的
                self.province_model.appendRow(item)
            elif item_code.endswith("00"):  # 2个0结尾的是市
                self.city_model.appendRow(item)
            else:  # 市以下
                self.county_model.appendRow(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CityLinkageWindow()
    w.show()
    sys.exit(app.exec_())