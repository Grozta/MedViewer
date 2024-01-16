#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import random
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QColorDialog, QMessageBox, QMenu, QAction, \
    QFileDialog

from LabelColor import LabelColor
from LabelEditorDialog import Ui_LabelEditorDialog
from util import CreateColorBoxIcon, get_base_dir

base_dir = get_base_dir()


class LabelEditorDialogWindow(QWidget, Ui_LabelEditorDialog):
    # TODO 排序列表的值
    def __init__(self, call_back=None):
        super(LabelEditorDialogWindow, self).__init__()
        self.call_back = call_back
        self.setupUi(self)
        self.center()
        self.setWindowTitle('Label Color')
        self.setWindowIcon(QIcon(os.path.join(base_dir, 'resources', 'HQU_logo1.png')))
        self.model = QStandardItemModel()
        self.lvLabels.setModel(self.model)
        self.lvLabels.clicked.connect(self.table_click)
        self.init()
        self.inRed.valueChanged.connect(self.red_change)
        self.inGreen.valueChanged.connect(self.green_change)
        self.inBlue.valueChanged.connect(self.blue_change)
        self.inLabelDescription.textChanged.connect(self.description_change)
        self.btnLabelColor.clicked.connect(self.color_click)
        self.inLabelId.editingFinished.connect(self.label_id_change)
        self.btnClose.clicked.connect(self.close_btn_click)
        self.btnNew.clicked.connect(self.new_btn_click)
        self.btnDelete.clicked.connect(self.delete_btn_click)

        menu = QMenu(self)
        self.actionImportLabel = QAction('import label description...', self)
        self.actionImportLabel.triggered.connect(self.import_label_click)
        self.actionExportLabel = QAction('export label description...', self)
        self.actionExportLabel.triggered.connect(self.export_label_click)
        menu.addAction(self.actionImportLabel)
        menu.addAction(self.actionExportLabel)
        self.btnActions.setMenu(menu)

    def closeEvent(self, event):
        """
        关闭事件
        :param event: 事件
        """
        if self.call_back:
            self.call_back()

    def close_btn_click(self):
        """
        关闭事件
        """
        self.close()

    def import_label_click(self):
        """
        导入标签
        """
        path = QFileDialog.getOpenFileName(self, 'Load Label Descriptions', '~', "Text Files (*.txt)")[0]
        if path != '':
            self.model.clear()
            LabelColor.read_file(path)
            self.init()

    def export_label_click(self):
        """
        导出标签
        """
        path = QFileDialog.getSaveFileName(self, 'Save Label Descriptions', '~', "Text Files (*.txt)")[0]
        print(path)
        if path != '':
            os.makedirs(os.path.dirname(path), exist_ok=True)
            LabelColor.to_file(path)

    def new_btn_click(self):
        """
        添加颜色标签事件
        """
        new_item = -1
        for i in range(1, 1 + 0xffffff):
            if i not in LabelColor.label2r:
                new_item = i
                break
        if new_item < 0:
            return
        self.cur = len(LabelColor.label2r)
        rgb = random.choice(list(set(range(1, 1 + 0xffffff)) - LabelColor.rgb2label_dict.keys()))
        r = rgb >> 16
        g = (rgb >> 8) & 0xff
        b = rgb & 0xff
        LabelColor.label2r[new_item] = r
        LabelColor.label2g[new_item] = g
        LabelColor.label2b[new_item] = b
        LabelColor.label2description[new_item] = f'Label {self.cur + 1}'
        LabelColor.rgb2label_dict[rgb] = new_item
        # 列表中的图标
        self.model.setItem(self.cur, 0, QStandardItem(QStandardItem(
            CreateColorBoxIcon(16, 16, r, g, b),
            str(new_item))))
        # 列表标签
        self.model.setItem(self.cur, 1, QStandardItem(LabelColor.label2description[new_item]))
        self.change_color(new_item, False)
        # 描述
        self.inLabelDescription.setText(LabelColor.label2description[new_item])
        # 标签的像素值
        self.inLabelId.setValue(new_item)
        self.lvLabels.selectRow(self.cur)
        self.lvLabels.setFocus()

    def delete_btn_click(self):
        """
        删除标签事件
        """
        label_len = len(LabelColor.label2r)
        if label_len <= 1:
            return
        k = int(self.model.item(self.cur, 0).text())
        r = LabelColor.label2r.pop(k)
        g = LabelColor.label2g.pop(k)
        b = LabelColor.label2b.pop(k)
        LabelColor.label2description.pop(k)
        LabelColor.rgb2label_dict.pop(r << 16 | g << 8 | b)
        self.model.removeRow(self.cur)
        self.cur = self.lvLabels.currentIndex().row()
        self.change_item_by_k(int(self.model.item(self.cur, 0).text()))

    def label_id_change(self):
        """
        修改标签对应的像素值事件
        """
        k = int(self.model.item(self.cur, 0).text())
        new_id = self.inLabelId.value()
        # 没有修改
        if new_id == k:
            return

        if new_id in LabelColor.label2r:
            self.msg = QMessageBox()
            self.msg.setWindowModality(Qt.NonModal)
            self.msg.setWindowTitle('warning')
            self.msg.setText(
                f'Can not change the numerical value to {new_id} because a label with that value already exists.')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()
            self.inLabelId.setValue(k)

            # self.lvLabels.selectRow(self.cur)
            # self.lvLabels.setFocus()
        else:
            # 删除原来的
            r = LabelColor.label2r.pop(k)
            g = LabelColor.label2g.pop(k)
            b = LabelColor.label2b.pop(k)
            d = LabelColor.label2description.pop(k)
            # 替换
            LabelColor.label2r[new_id] = r
            LabelColor.label2g[new_id] = g
            LabelColor.label2b[new_id] = b
            LabelColor.label2description[new_id] = d
            LabelColor.rgb2label_dict[r << 16 | g << 8 | b] = new_id
            # 列表中的图标
            self.model.setItem(self.cur, 0, QStandardItem(QStandardItem(
                CreateColorBoxIcon(16, 16, r, g, b),
                str(new_id))))
            self.inLabelId.setValue(new_id)

    def color_click(self):
        """
        按钮修改颜色事件
        """
        k = int(self.model.item(self.cur, 0).text())
        col = QColorDialog.getColor()
        LabelColor.label2r[k] = col.red()
        LabelColor.label2g[k] = col.green()
        LabelColor.label2b[k] = col.blue()
        self.change_color(k)

    def description_change(self):
        """
        修改标签的描述事件
        """
        k = int(self.model.item(self.cur, 0).text())
        LabelColor.label2description[k] = self.inLabelDescription.text()
        # 修改列表标签
        self.model.setItem(self.cur, 1, QStandardItem(LabelColor.label2description[k]))

    def red_change(self):
        """
        红色像素值修改事件
        """
        k = int(self.model.item(self.cur, 0).text())
        LabelColor.label2r[k] = self.inRed.value()
        self.change_color(k)

    def green_change(self):
        """
        绿色像素值修改事件
        """
        k = int(self.model.item(self.cur, 0).text())
        LabelColor.label2g[k] = self.inGreen.value()
        self.change_color(k)

    def blue_change(self):
        """
        蓝色像素值修改事件
        """
        k = int(self.model.item(self.cur, 0).text())
        LabelColor.label2b[k] = self.inBlue.value()
        self.change_color(k)

    def init(self):
        """
        初始化列表
        """
        self.cur = 0
        for i, k in enumerate(LabelColor.label2r.keys()):
            # 列表中的图标
            self.model.setItem(i, 0, QStandardItem(QStandardItem(
                CreateColorBoxIcon(16, 16, LabelColor.label2r[k], LabelColor.label2g[k], LabelColor.label2b[k]),
                str(k))))
            # 列表标签
            self.model.setItem(i, 1, QStandardItem(LabelColor.label2description[k]))
            if self.cur == i:
                self.change_item_by_k(k)
        self.lvLabels.selectRow(0)
        self.lvLabels.setFocus()

    def change_color(self, k, icon_flag=True):
        """
        根据当前标签的像素值，修改右边和左边的标签的颜色

        :param k: 当前标签的像素值
        :param icon_flag: 是否修改标签的颜色
        """
        # 颜色
        self.inRed.setValue(LabelColor.label2r[k])
        self.inGreen.setValue(LabelColor.label2g[k])
        self.inBlue.setValue(LabelColor.label2b[k])
        # 按钮图标
        self.btnLabelColor.setIcon(
            CreateColorBoxIcon(16, 16, LabelColor.label2r[k], LabelColor.label2g[k], LabelColor.label2b[k]))
        # TODO 改成转盘
        self.inColorWheel.setStyleSheet(
            f'background-color: rgb({LabelColor.label2r[k]},{LabelColor.label2g[k]},{LabelColor.label2b[k]});')
        if icon_flag:
            # 列表中的图标
            self.model.setItem(self.cur, 0, QStandardItem(QStandardItem(
                CreateColorBoxIcon(16, 16, LabelColor.label2r[k], LabelColor.label2g[k], LabelColor.label2b[k]),
                str(k))))

    def change_item_by_k(self, k):
        """
        根据当前标签的像素值，修改右边

        :param k: 当前标签的像素值
        """
        k = int(k)
        self.change_color(k, False)
        # 描述
        self.inLabelDescription.setText(LabelColor.label2description[k])

        # 标签的像素值
        self.inLabelId.setValue(k)

    def table_click(self, item):
        """
        列表点击事件

        :param item: 当前点击的
        """
        self.cur = item.row()
        self.change_item_by_k(self.model.item(self.cur, 0).text())

    def center(self):
        """
        界面居中显示
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LabelEditorDialogWindow()
    ex.show()
    sys.exit(app.exec_())
