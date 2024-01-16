#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from Operative.ui.load_img2 import Ui_Form
from util import get_base_dir

base_dir = get_base_dir()


class playimg2(QWidget, Ui_Form):
    def __init__(self, parent=None, data_path=None):
        super(playimg2, self).__init__(parent)
        self.setupUi(self)
        self.n = 0
        self.data_path = data_path
        self.origin_files = os.listdir(self.data_path)
        self.origin_files.sort()
        self.setWindowTitle('微创手术器械识别与分割')
        self.setWindowIcon(QIcon(os.path.join(base_dir, 'resources', 'HQU_logo1.png')))
        print("init finished")

        self.num = len(self.origin_files)
        self.btn_play.clicked.connect(self.play_set)
        self.btn_last.clicked.connect(self.play_last)
        self.btn_next.clicked.connect(self.play_next)
        self.timer1 = QTimer()
        self.timer1.start(500)
        self.timer1.timeout.connect(self.timer_TimeOut)
        self.center()

    def center(self):
        """
        界面居中显示
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def play_set(self):
        if self.btn_play.text() == '播放':
            self.timer1 = QTimer()
            self.timer1.timeout.connect(self.timer_TimeOut)
            self.timer1.start(500)
            self.btn_play.setText('暂停')
        else:
            self.timer1.stop()
            self.btn_play.setText('播放')

    def play_next(self):
        self.timer1.stop()
        self.timer_TimeOut()
        self.btn_play.setText('播放')

    def play_last(self):
        self.timer1.stop()
        self.n -= 1
        self.btn_play.setText('播放')
        if self.n < 0:
            self.n = len(self.origin_files) - 1
        self.n -= 1
        if self.n < 0:
            self.n = len(self.origin_files) - 1
        self.timer_TimeOut()

    def timer_TimeOut(self):
        self.n += 1
        if self.n >= len(self.origin_files):
            self.n = 0
        label = self.img1
        pixmap = QPixmap(os.path.join(self.data_path, self.origin_files[self.n]))
        pixmap = pixmap.scaled(label.width(), label.height())  ##固定图片大小与label一样
        label.setPixmap(pixmap)  # 加载图片
        label.setScaledContents(True)  # 自适应
