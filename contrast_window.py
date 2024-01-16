#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QMessageBox

from contrast import Ui_Widget
from util import get_base_dir

base_dir = get_base_dir()


class ContrastWindow(QWidget, Ui_Widget):
    def __init__(self, minimum, maximum, window, level, callback):
        super(ContrastWindow, self).__init__()
        self.callback = callback
        self.setupUi(self)
        self.center()
        self.setWindowTitle('Contrast')
        self.setWindowIcon(QIcon(os.path.join(base_dir, 'resources', 'HQU_logo1.png')))
        self.minimum = minimum
        self.maximum = maximum
        self.level_spinBox.setMinimum(minimum)
        self.level_spinBox.setMaximum(maximum)
        self.level_spinBox.setValue(level)
        self.window_spinBox.setMinimum(0)
        self.window_spinBox.setMaximum(maximum - minimum)
        self.window_spinBox.setValue(window)
        self.apply_pushButton.clicked.connect(self.apply_event)
        self.ok_pushButton.clicked.connect(self.ok_event)
        self.reset_pushButton.clicked.connect(self.reset_event)

    def closeEvent(self, event):
        """
        关闭事件
        :param event: 事件
        """
        if self.callback:
            self.callback(self.window_spinBox.value(), self.level_spinBox.value())

    def apply_event(self):
        """
        应用事件
        """
        if self.callback:
            self.callback(self.window_spinBox.value(), self.level_spinBox.value())

    def ok_event(self):
        """
        确认事件
        """
        # if self.callback:
        #     self.callback(self.window_spinBox.value(), self.level_spinBox.value())
        self.close()

    def reset_event(self):
        """
        重置窗宽窗位事件
        """
        self.level_spinBox.setValue((self.minimum + self.maximum) // 2)
        self.window_spinBox.setValue(self.maximum - self.minimum)
        if self.callback:
            self.callback(self.window_spinBox.value(), self.level_spinBox.value())

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
    ex = ContrastWindow()
    ex.show()
    sys.exit(app.exec_())
